# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:13:17 2022

@author: Konstantinos Pattakos
"""

import requests
import re
import pandas as pd

def parse_game(url):
    page = requests.get(url)
    string = page.text
    title = re.findall(r'<title>(.*?) \| Board Game \| BoardGameGeek</title>', string)[0]
    # print(title)
    gametype = re.findall('\"boardgamesubdomain\"\:\[\{\"name\"\:\"(.*?) Games\"', string)[0]
    # print('TYPE:', gametype)
    categories = re.findall(r'\"boardgamecategory\":\[(.*?)\]', string)
    min_pl = re.findall('minplayers\"\:\"(.*?)\"', string)[0]
    max_pl = re.findall('maxplayers\"\:\"(.*?)\"', string)[0]
    min_time = re.findall('minplaytime\"\:\"(.*?)\"', string)[0]
    max_time = re.findall('maxplaytime\"\:\"(.*?)\"', string)[0]
    mean_time = (int(min_time) + int(max_time))/2
    weight = re.findall(r'\"averageweight\"\:(.*?),', string)[0]
    image = re.findall(r'\"image\"\: \"(.*?)\"', string)[0]
    rank = re.findall(r'\,\"rank\":\"(.*?)\",', string)[0]
    # print(image)"description":"<p>
    description = re.findall(r'\"description\"\:\"\<p\>(.*?)\\n', string)[0]
    description = re.sub(r"\<(.*?)\>", "", description)
    description = re.sub(r"  ", " ", description)
    rating = re.findall(r'\"ratingValue\"\: \"(.*?)\"', string)[0]
    cat = re.findall(r'\{\"name\"\:\"(.*?)\"', categories[0])
    for c in cat:
        try:
            c = re.sub(r"\\", "", c)
        except:
            pass
        print(c)
    info = dict()
    info['title'] = title 
    info['type'] = gametype
    info['rank'] = int(rank)
    info['rating'] = float(rating)
    info['mean time'] = int(mean_time) 
    info['min players'] = int(min_pl)
    info['max players'] = int(max_pl)
    info['category 1'] = cat[0]
    try:
        info['category 2'] = cat[1]          
    except:
        info['category 2'] = '-'
        # pass
    try:
        info['category 3'] = cat[2]
    except:
        info['category 3'] = '-'
        # pass
    info['weight'] = float(weight)
    info['description'] = description
    info['image'] = image
    
    # print('Min players:' ,min_pl, 'Max players:' ,max_pl, 'Mean time:', mean_time)
    # print('Categories:', info['category 1']+',', info['category 2']+',', info['category 3'])
    # print(description)
    # print()
    df = pd.DataFrame.from_records([info])
    return df

URL = "https://boardgamegeek.com/browse/boardgame/page/1"
page = requests.get(URL)
string = page.text

# print(page.text)

pattern = r'class=\'primary\' >(.*)<'

games = re.findall(pattern, string)

href = re.findall(r'href=\"\/boardgame(.*?)"', string)
href = href[::3]

# href = href[:10]

sum_df = []
for h in href:
    URL = f'https://boardgamegeek.com/boardgame{h}'
    info = parse_game(URL)
    info['link'] = URL
    sum_df.append(info)

df = pd.concat(sum_df)

category1 = df['category 1'].tolist()
category2 = df['category 2'].tolist()
category3 = df['category 3'].tolist()

cats = category1 + category2 + category3
#%%
output = open('cats.txt', 'w')
for c in cats:
    output.write(c + "\n")
    print((c))



