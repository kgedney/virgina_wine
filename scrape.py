#!/usr/bin/env python

"""
    scrape.py
    
    From 'https://www.virginiawine.org/governors-cup/awards'
    2023 only
"""

# -- prep
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from rich import print
from tqdm import tqdm

# -- get list of wines

def parse_item(item):
    try:
        medal  = item.find("i", {"class" : "fa-circle"}).get('class')[-1].split('-')[-1]
        
        if item.find('a') is not None:
            winery = item.find("a").text
            href   = item.find('a').get('href')
            wine   = item.find_all('span')[-1].text
        else:
            spans  = item.find('span', {"class" : "winner-list__body"}).find_all('span')
            winery = spans[0].text
            wine   = spans[1].text
            href   = None
        
        if href is not None:
            url = f'https://www.virginiawine.org/{href}'
        else:
            url = None
        
        return {
            "medal"  : medal,
            "winery" : winery,
            "wine"   : wine,
            "url"    : url
        }
    except:
        print(item)
        raise Exception()


x    = 'https://www.virginiawine.org/governors-cup/awards/2023'
res  = requests.get(x)
soup = BeautifulSoup(res.text)

data  = soup.find("div", {"id": "winner_list"})
items = soup.find_all("li", {"class" : "winner-list__item"})
df    = pd.DataFrame([parse_item(item) for item in items])

df.url.unique().shape

# -- get wineries

def parse_vineyard(soup):
    address = re.sub(r'\n +', '\n', soup.find('address').text.strip())
    lat     = soup.find("div", {'class': 'card__map'}).get('data-lat')
    lon     = soup.find("div", {'class': 'card__map'}).get('data-lng')
    return {
        "address" : address,
        "lat"     : lat,
        "lon"     : lon,
    }

vineyard_html = {}
df_address    = []

for url in tqdm(df.url.unique()):
    if url is None: continue
    if url in vineyard_html: continue
    
    res  = requests.get(url)
    vineyard_html[url] = res.text # add to dictionary with raw html
    soup = BeautifulSoup(res.text)
    addr = parse_vineyard(soup)
    addr['url'] = url
    df_address.append(addr)

df_address = pd.DataFrame(df_address)

# -- save data

df.to_csv('wines.tsv', sep='\t', index=None)
df_address.to_csv('wineries.tsv', sep='\t', index=None)
_ = open('wineries_raw.json', 'w').write(json.dumps(vineyard_html))
