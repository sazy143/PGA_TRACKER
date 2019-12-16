import argparse
from webScrapper import webScrapper

parser = argparse.ArgumentParser(description='controller to decide what urls to scrap, and where to put that data')

parser.add_argument("-o", help='The file to write the json data to.')
parser.add_argument("-i", required=True, help='The input URL or file to read data from')
parser.add_argument("-d", choices=['True','False'], help='If set will save data to database ("True" or "False")')
parser.add_argument("-s", choices=['leaderboard','schedule','fedex'], required=True, help='The scrapper to use ("leaderboard","schedule","fedex")')

args = parser.parse_args()

output = args.o
inputt = args.i
database = args.d
scrapper = args.s 

print(output,inputt,database,scrapper)
scrape = webScrapper(inputt, scrapper, output, database)
scrape.execute()
