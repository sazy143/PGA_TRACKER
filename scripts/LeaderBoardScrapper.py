from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
from selenium.webdriver.firefox.options import Options
import json

def playerObject(data):
    name = data[2].text.replace(u'\xa0',' ').strip()
    player = {}
    player['position'] = data[0].text.strip()
    player['events'] = data[3].text.strip()
    player['points'] = data[4].text.strip()
    player['wins'] = data[5].text.strip()
    player['top10'] = data[6].text.strip()
    players[name] = player

# your custom input to direct the flow 
# note this script is for getting tournament data

#************* ONLY NEED TO CHANGE INBETWEEN THESE LINES **************

# Fill out the option you would like to use other wise leave blank
url = ""
yourFile = "fedex.txt"

# the location to output the file to format is /path/filename.txt
path = '../src/jsonFiles/fedex.json'

#**********************************************************************

pagesource = ''

# ********THIS SECTION FOR EXTRACTING PAGE SOURCE ***************
try:
    options = Options()
    # dont actually open a web browser
    options.add_argument('-headless')

    # create driver
    driver = webdriver.Firefox(options=options)
    # get the page
    driver.get(url)
    # extract the page source (html)
    pagesource = driver.page_source
    print('from web')
except:
# read from the text file you specified
    try:
        with open(yourFile,'r') as f:
            pagesource = f.read()
        print('from file')
    except:
        print('no input given')
        exit()

# save the source data to a text file so we do not have to keep pinging the site when developing/testing
# with open(yourFile,'w',encoding='utf-8') as f:
#     f.write(pagesource)

# data to collect
players = {}

# create a soup object with our page source
soup = BeautifulSoup(pagesource, 'lxml')

playerTable = soup.find_all("table","table-fedexcup-standings")
playerTable = playerTable[0]

playersTR = playerTable.find_all("tr")

for player in playersTR:
    info = player.find_all("td")
    if(len(info)>8):
        playerObject(info)

# prints all player info nicely
# for player in players:
#     print(player)
#     for info in players[player]:
#         print(info,':', players[player][info])

# variable to store all the data we want to make into a json
jsonObject = {}
# add our data to the dictionary
jsonObject['players'] = players

# write to json file the data we have scraped
with open(path, 'w' )as f:
    json.dump(jsonObject, f, ensure_ascii=False)