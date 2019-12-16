#coding utf8
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
from selenium.webdriver.firefox.options import Options
import json
import re
import sys
import os
sys.path.append(os.path.abspath('./database'))
from PGA_CRUD import PGA_CRUD

class webScrapper:
    # object initialization
    def __init__(self, input, scrapper, output=None, saveToDB = None):
        self.input = input
        self.output = output
        self.pagesource = None
        self.json = {}
        self.scrapper = scrapper
        self.saveToDB = saveToDB
        if(saveToDB):
            self.database = PGA_CRUD()

    # main function to execute everything
    def execute(self):
        if("http" in self.input):
            try:
                self.fromWeb()
            except:
                print('Error in getting contents from the web')
        else:
            try:
                self.fromTxt()
            except:
                print('Error in reading from file')
        if(self.pagesource== None):
            print('no page source exiting program')
            exit()
        if(self.scrapper=='schedule'):
            self.scheduleScrapper()
        elif(self.scrapper=='fedex'):
            self.fedexScrapper()
        elif(self.scrapper=='leaderboard'):
            self.leaderboardScrapper()

        if self.output == None:
            print("do nothing")
        elif ".json" in self.output :
            self.saveToFile()
        else:
            print('save file must be a json')

        if(self.saveToDB):
            if self.scrapper == 'schedule':
                for key in self.json:
                    results = self.database.update('tournaments', {'name':key}, self.json[key])
                    print(results)

            elif self.scrapper == 'fedex':
                players = self.json['players']
                for player in players:
                    result = self.database.update('players',{'name':player['name']},{'$set': player})

            elif self.scrapper == 'leaderboard':
                tournament = self.json['tournament']
                players = self.json['players']
                result = self.database.update('tournaments',{'name':tournament},{'$set': {'players': players}})
                print(result)
                
                

    # get pagesource if input is a url
    def fromWeb(self):
        # create options for webdriver
        options = Options()
        options.add_argument('-headless')
        # create driver
        driver = webdriver.Firefox(options=options)
        # get the url
        driver.get(self.input)
        # save the page content to our variable
        self.pagesource = driver.page_source

    # get page source if input is a file
    def fromTxt(self):
        # open text file and read data into page source variable
        with open(self.input, 'r') as f:
            self.pagesource = f.read()

    # save results into a file
    def saveToFile(self):
        # result is json so dump it into a file
        with open(self.output, 'w') as f:
            json.dump(self.json,f,ensure_ascii=False)

    # function to use if we are getting schedule info
    def scheduleScrapper(self):
        # top level json object (dictionary)
        tournaments = {}
        # put into soup object
        soup = BeautifulSoup(self.pagesource, 'lxml')
        # find the specific table
        tables = soup.find_all("table","table-styled")
        # what we want is the first result from the find all
        table = tables[0]
        # get all the table rows
        rows = table.find_all("tr")
        # scan over every row in rows
        for row in rows:
            # get the table data
            data = row.find_all("td")
            # if the row has the amount of data we want we will search for our data
            if(len(data)>5):
                # dictionary to hold specific tournament data
                tournament = {}
                # get the data from the table data and add to dictionary
                date = ' '.join(data[0].text.split())
                tournament['date'] = date
                # get the tag to be able to find leaderboard url
                hrefs = data[1].find_all(href = True)
                if(len(hrefs)>0):
                    # assuming first href is the right one 
                    url = hrefs[0]['href']
                    tag = url[url.find('tournaments/')+len('tournaments/'):url.find(".")]
                    tournament['tag'] = tag
                # get the amount of fedex points and add to dictionary
                points = data[5].text.strip()
                tournament['points'] = points
                # convert td1 to string
                string = data[1].text
                # split it based on parameter
                s1 = string.split("    ")
                # get rid of white space on tournament name
                name = s1[0].strip()
                tournament['name'] = name
                # remove tournament name from original string
                string = string.replace(name,"")
                # split is based on &nbsp 
                s2 = string.split(u"\xa0")
                # get rid of white space and add to dictionary
                course = s2[0].strip()
                tournament['course'] = course
                # if there are 5 parameter the last one is the purse
                if(len(s2)>4):
                    # get the purse amount and add to dictionary
                    purse = s2[4].strip()[8:].replace(","," ")
                    tournament['purse'] = purse
                tournament['players'] = []
                # add our tournament data to our tournaments dictionary
                tournaments[name] = tournament
        self.json = tournaments

    def leaderboardScrapper(self):
        players = []
        # create a soup object with our page source
        soup = BeautifulSoup(self.pagesource, 'lxml')
        # find specific h1 tags
        tournamentHeader = soup.find_all("h1","name")
        # what we want is the first result from the find all
        tournament = tournamentHeader[0].text
        # extract all the tables based on class='leaderboard'
        tournamentPlayerTables = soup.find_all("table", "leaderboard")
        # variable to hold all the tr tags found
        playersTR = []
        # get the all trs and store them in array declared above
        for table in tournamentPlayerTables:
            list = table.find_all("tr")
            for player in list:
                playersTR.append(player)
        for player in playersTR:
            data = player.find_all("td")
            if(len(data) > 12):
                name = re.sub(r'\(\w+\)',"",data[4].text).strip()
                player = {}
                player['position'] = data[1].text
                player['score'] = data[5].text
                player['round1'] = data[8].text
                player['round2'] = data[9].text
                player['round3'] = data[10].text
                player['round4'] = data[11].text
                player['name'] = name
                players.append(player)
        jsonObject = {}
        # add our data to the dictionary
        jsonObject['tournament'] = tournament.strip()
        jsonObject['players'] = players
        self.json = jsonObject

    def fedexScrapper(self):
        # data to collect
        players = []
        # create a soup object with our page source
        soup = BeautifulSoup(self.pagesource, 'lxml')
        playerTable = soup.find_all("table","table-fedexcup-standings")
        playerTable = playerTable[0]
        playersTR = playerTable.find_all("tr")
        for player in playersTR:
            data = player.find_all("td")
            if(len(data)>8):
                    name = data[2].text.replace(u'\xa0',' ').strip()
                    player = {}
                    player['position'] = data[0].text.strip()
                    player['events'] = data[3].text.strip()
                    player['points'] = data[4].text.strip()
                    player['wins'] = data[5].text.strip()
                    player['top10'] = data[6].text.strip()
                    player['name'] = name
                    players.append(player)
        # variable to store all the data we want to make into a json
        jsonObject = {}
        # add our data to the dictionary
        jsonObject['players'] = players
        self.json = jsonObject