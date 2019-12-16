from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
from selenium.webdriver.firefox.options import Options
import json

# your custom input to direct the flow 
# note this script is for getting tournament data

#************* ONLY NEED TO CHANGE INBETWEEN THESE LINES **************

# Fill out the option you would like to use other wise leave blank
url = ""
yourFile = ""

# the location to output the file to format is /path/filename.txt
path = '../src/jsonFiles/current.json'

#**********************************************************************

# put player data into a dictionary to act like an object and append it to 
# the players dictionary (2d dictionary)
def playerObject(data):
    name = data[4].text
    player = {}
    player['position'] = data[1].text
    player['score'] = data[5].text
    player['round1'] = data[8].text
    player['round2'] = data[9].text
    player['round3'] = data[10].text
    player['round4'] = data[11].text
    players[name] = player

# data to collect
tournament = ''
players = {}

# variable to hold the page data
pagesource = ''

# ********THIS SECTION FOR EXTRACTING PAGE SOURCE ***************
try:
    options = Options()
    # dont actually open a web browser
    options.headless = True

    # create driver
    driver = webdriver.Firefox(options=options)
    # get the page
    driver.get(url)
    # extract the page source (html)
    pagesource = driver.page_source
except:
# read from the text file you specified
    try:
        with open(yourFile,'r') as f:
            pagesource = f.read()

    except:
        print('no input given')
        exit()

# save the source data to a text file so we do not have to keep pinging the site when developing/testing
# with open('leaderboard.txt','w',encoding='utf-8') as f:
#     f.write(driver.page_source)







# create a soup object with our page source
soup = BeautifulSoup(pagesource, 'lxml')

# variable to hold tournament names found in page
tournamentNames = []

# find specific h1 tags
tournamentHeader = soup.find_all("h1","name")
# parse through those tags extracting the text and storing it in previously declared variable
for h1 in tournamentHeader:
    tournamentNames.append(h1.text)

# incase multiple are found we have deduced that the data we want is the first result found
tournament = tournamentNames[0]

# extract all the tables based on class='leaderboard'
tournamentPlayerTables = soup.find_all("table", "leaderboard")

# variable to hold all the tr tags found
playersTR = []

# get the all trs and store them in array declared above
for table in tournamentPlayerTables:
    list = table.find_all("tr")
    for player in list:
        playersTR.append(player)

# get all the data from the tr's and if it matches player criteria run playerObect function
# which will put it in the dictionary to be in our final results
for player in playersTR:
    data = player.find_all("td")
    if(len(data) > 12):
        playerObject(data)
    
# prints all player info nicely
# for player in players:
#     print(player)
#     for info in players[player]:
#         print(info,':', players[player][info])
    
#     print()

# variable to store all the data we want to make into a json
jsonObject = {}
# add our data to the dictionary
jsonObject['tournament'] = tournament.strip()
jsonObject['players'] = players

# write to json file the data we have scraped
with open(path, 'w' )as f:
    json.dump(jsonObject, f, ensure_ascii=False)
