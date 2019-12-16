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
yourFile = "schedule.txt"

# the location to output the file to format is /path/filename.txt
path = '../src/jsonFiles/schedule.json'

#**********************************************************************

#pagesource = ''

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

# info to collect
tournaments = {}

# create a soup object with our page source
soup = BeautifulSoup(pagesource, 'lxml')

# find specific table tags
tables = soup.find_all("table","table-styled")
# only one result should be found so put it in a variable
table = tables[0]

# get all the table rows
rows = table.find_all("tr")

def scuffedWorkaround(tournament,inconsequential):
    
    string = inconsequential.text
    s1 = string.split("   ")
    part1 = s1[0].strip()
    string = string.replace(part1,"")
    s2 = string.split(u"\xa0")
    course = s2[0].strip()
    tournament['course'] = course
    if(len(s2)>4):
        purse = s2[4].strip()[8:].replace(","," ")
        tournament['purse'] = purse
    tournaments[part1] = tournament


# extract data from each table row
for row in rows:
    data = row.find_all("td")

    if(len(data)>5):
        tournament = {}
        date = ' '.join(data[0].text.split())
        tournament['date'] = date
        points = data[5].text.strip()
        tournament['points'] = points
        # handle and put the data in a nice usable json format
        scuffedWorkaround(tournament,data[1])

with open(path,'w') as f:
    json.dump(tournaments,f,ensure_ascii=False)