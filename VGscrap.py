from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import re


df = pd.DataFrame(columns=["title", "user_Score", "release_Date", "console", "url",
                           "publisher", "developer", "tot_ship", 'tot_sale','na_sale','pal_sale','jp_sale',
                           'other_sale', 'last_update', 'VGscore'])    

page = 1
urlprefix = 'http://www.vgchartz.com/games/games.php?page='
urlsuffix = '&results=1000&name=&console=&keyword=&publisher=&genre=&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=Yes'

with requests.Session() as session:
       while page < 57:
              url = urlprefix + str(page) + urlsuffix
              try:     
                     req = Request(url, headers ={'User-Agent':'Mozilla/5.0'})
                     page1 = urlopen(req)
                     if page1.getcode() == 200:
                            webpage = page1.read()
                            page_soup = soup(webpage, "html.parser")
                            main = page_soup.findAll("tr", {'style': re.compile('background.*')})
              
                            for row in main:
                                   ahref = row.findAll("a", href = True)[1].contents[0]
                                   url = row.findAll("a", href = True)[1]['href']
                                   console = row.findAll("img", alt = True)[1]['alt']
                                   tdcontainer = row.findAll('td')
                                   publisher = tdcontainer[4].contents[0]
                                   developer = tdcontainer[5].contents[0]
                                   VGscore = tdcontainer[6].contents[0]
                                   user_score = tdcontainer[8].contents[0]
                                   tot_ship = tdcontainer[9].contents[0]
                                   tot_sale = tdcontainer[10].contents[0]
                                   na_sale = tdcontainer[11].contents[0]
                                   pal_sale = tdcontainer[12].contents[0]
                                   jp_sale =  tdcontainer[13].contents[0],
                                   other_sale = tdcontainer[14].contents[0]
                                   release_date = tdcontainer[15].contents[0]
                                   last_update = tdcontainer[16].contents[0]
                                   game_data = {'title':[ahref], "console":[console], "user_Score":[user_score], "VGscore":[VGscore], "release_Date": [release_date], "publisher":[publisher],
                                                 "developer":[developer],"tot_ship": [tot_ship],"tot_sale": [tot_sale], "na_sale":[na_sale], "pal_sale":[pal_sale],
                                                 "jp_sale": [jp_sale], "other_sale": [other_sale], "last_update": [last_update], "url":[url]}
                                   df = df.append(pd.DataFrame(data = game_data), sort = False).reset_index(drop = True)
              except Exception as inst:
                     print (inst)
                     print (page)

              try:     
                     for game in df['url']:
                            req = Request(game.replace("?region=All", "sales"), headers ={'User-Agent':'Mozilla/5.0'})
                            page1 = urlopen(req)
                            if page1.getcode() == 200:
                                   webpage = page1.read()
                                   page_soup = soup(webpage, "html.parser")
                                   main = page_soup.find("div", {'id': 'gameGenInfoBox'})
                                   genre = main.findAll('p')[3].contents[0]
                                   sales = page_soup.findAll('div', {'id': 'gameSalesBox'})
                                   if sales:
                                          

                     page += 1
                     print ("Done " + str(page))
                     
print ("Done")
df.to_csv("vgscore.csv", index = False)  
    


           