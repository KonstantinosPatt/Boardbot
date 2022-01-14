# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:13:17 2022

@author: Konstantinos Pattakos
"""

import requests
import re
import pandas as pd
from parse_game import parse_game

URL = "https://boardgamegeek.com/browse/boardgame/page/1"
page = requests.get(URL)
string = page.text

# print(page.text)

pattern = r'class=\'primary\' >(.*)<'

games = re.findall(pattern, string)

href = re.findall(r'href=\"\/boardgame(.*?)"', string)
href = href[::3]

href = href[:10]

sum_df = []
for h in href:
    URL = f'https://boardgamegeek.com/boardgame{h}'
    info = parse_game(URL)
    info['link'] = URL
    sum_df.append(info)

df = pd.concat(sum_df)