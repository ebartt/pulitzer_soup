import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import urllib.parse
from time import sleep
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

root_url = 'https://en.wikipedia.org/wiki/Pulitzer_Prize_for_Fiction#1980s_to_present'
base_url = 'https://en.wikipedia.org/'

def get_data():  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get(root_url, headers=headers)
    content = r.content
    soup = BeautifulSoup(content)

    #navigating to the table with winners from 1980 to present
    listtables = soup.find_all('table')
    table = listtables[4].find_all('tr')

    all = []

    for row in table:
        yeartag = row.find('th') if row.find('th') is not None else None
        if yeartag is not None:
            year = yeartag.get_text(strip = True)
            winner = 1
        else:
            year = None
            winner = 0
        
        #getting all elems in a list
        elems = row.find_all('td')
        if len(elems) > 1:
            author_tag = elems[0]
            title_tag = elems[1]

            author = author_tag.get_text(strip = True)
            title = title_tag.get_text(strip = True)
            title_href = title_tag.find('a').get('href') if title_tag.find('a') is not None else None
            # if len(elems) >= 3:
            #     genretag = elems[2]
            #     genres.append(genretag.get_text(strip = True))
        else:
            author = None
            title = None
            title_href = None

        if title_href is not None:
                book_page = requests.get(base_url + title_href, headers=headers)
                book_soup = BeautifulSoup(book_page.content)
                
                infobox = book_soup.find('table', attrs = {'class': "infobox ib-book vcard"})
                if infobox is not None:
                    infobox_vals = infobox.find_all('tr')
                    for row in infobox_vals:
                        lab = row.find('th')
                        val = row.find('td')
                        if lab is not None:
                            rowlab = lab.get_text(strip = True)
                            if rowlab == "Publisher":
                                publisher = val.get_text(strip = True)
                            elif rowlab == 'Publication date' or rowlab == "Published":
                                pub_date = val.get_text(strip = True)
                            elif rowlab == 'Genre':
                                genre = val.get_text(strip = False) + ', Fiction'
                            elif rowlab == 'Media type':
                                media_type = val.get_text(strip = True)
                        else:
                            genre = "Fiction"
        else:
            publisher = None
            pub_date = year
            genre = 'Fiction'
            media_type = None

        all.append({
            'year': year,
            'auth': author,
            'title': title,
            'winner': winner,
            'publisher': publisher,
            'pub_date': pub_date,
            'genre': genre,
            'media_type': media_type if media_type else None
        })
    #<a class="kc-cover-link app-specific-display not_app" href="/dp/B0FJTF5MJB/ref=chrt_bk_sd_fc_1_ci_lp"> <img alt="Cover image of Dear Debbie by Freida McFadden" src="https://m.media-amazon.com/images/I/81K9E2AyfjL.jpg" title="Cover image of Dear Debbie by Freida McFadden"/>
    return all