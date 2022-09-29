cookies = {
    '_ga_GMNMCY4DVM': 'GS1.1.1663858457.6.1.1663859943.0.0.0',
    '_ga': 'GA1.2.853498761.1663780246',
    '_gid': 'GA1.2.113400907.1663780246',
    'cc_cookie': '%7B%22level%22%3A%5B%22necessary%22%2C%22analytics%22%2C%22shopping%22%2C%22socialmedia%22%5D%2C%22revision%22%3A1%2C%22data%22%3Anull%2C%22rfc_cookie%22%3Atrue%7D',
    'bggusername': 'Johnny%20Plunders',
    'bggpassword': 'uz7ezz89khh106d2morgk6mhxggttm31z',
    'SessionID': 'a78fcd6a2b32b46bd8a5f8a29b42a78f56bcbba2u761400',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Alt-Used': 'boardgamegeek.com',
    'Connection': 'keep-alive',
    'Referer': 'https://boardgamegeek.com/',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_ga_GMNMCY4DVM=GS1.1.1663858457.6.1.1663859943.0.0.0; _ga=GA1.2.853498761.1663780246; _gid=GA1.2.113400907.1663780246; cc_cookie=%7B%22level%22%3A%5B%22necessary%22%2C%22analytics%22%2C%22shopping%22%2C%22socialmedia%22%5D%2C%22revision%22%3A1%2C%22data%22%3Anull%2C%22rfc_cookie%22%3Atrue%7D; bggusername=Johnny%20Plunders; bggpassword=uz7ezz89khh106d2morgk6mhxggttm31z; SessionID=a78fcd6a2b32b46bd8a5f8a29b42a78f56bcbba2u761400',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

def parse_game(url):
    page = requests.get(url, cookies=cookies, headers=headers)
    string = page.text
    title = re.findall(r'<title>(.*?) \| Board Game \| BoardGameGeek</title>', string)[0]
    try:
        gametype = re.findall('\"boardgamesubdomain\"\:\[\{\"name\"\:\"(.*?) Games\"', string)[0]
    except:
        try:
            gametype = re.findall('\"boardgamesubdomain\"\:\[\{\"name\"\:\"(.*?)\"', string)[0]
        except:
            gametype = '-'
    categories = re.findall(r'\"boardgamecategory\":\[(.*?)\]', string)
    min_pl = re.findall('minplayers\"\:\"(.*?)\"', string)[0]
    max_pl = re.findall('maxplayers\"\:\"(.*?)\"', string)[0]
    min_time = re.findall('minplaytime\"\:\"(.*?)\"', string)[0]
    max_time = re.findall('maxplaytime\"\:\"(.*?)\"', string)[0]
    mean_time = (int(min_time) + int(max_time))/2
    weight = re.findall(r'\"averageweight\"\:(.*?),', string)[0]
    image = re.findall(r'\"image\"\: \"(.*?)\"', string)[0]
    rank = re.findall(r'\,\"rank\":\"(.*?)\",', string)[0]
    try:        
        description = re.findall(r'\"description\"\:\"\<p\>(.*?)\\n', string)[0]
        description = re.sub(r"\<(.*?)\>", "", description)
        description = re.sub(r"  ", " ", description)
    except:
        pass
    rating = re.findall(r'\"ratingValue\"\: \"(.*?)\"', string)[0]
    cat = re.findall(r'\{\"name\"\:\"(.*?)\"', categories[0])
    for c in cat:
        try:
            c = re.sub(r"\\", "", c)
        except:
            pass
        # print(c)
    info = dict()
    info['title'] = title 
    info['type'] = gametype
    info['rank'] = int(rank)
    info['rating'] = float(rating)
    info['mean time'] = int(mean_time) 
    info['min players'] = int(min_pl)
    info['max players'] = int(max_pl)
    try:
        info['category 1'] = cat[0]
    except:
        info['category 1'] = '-'
    try:
        info['category 2'] = cat[1]          
    except:
        info['category 2'] = '-'
    try:
        info['category 3'] = cat[2]
    except:
        info['category 3'] = '-'
    info['weight'] = float(weight)
    try:
        info['description'] = description
    except:
        info['description'] = '-'
    info['image'] = image
    
    # print('Min players:' ,min_pl, 'Max players:' ,max_pl, 'Mean time:', mean_time)
    # print('Categories:', info['category 1']+',', info['category 2']+',', info['category 3'])
    # print(description)
    # print()
    df = pd.DataFrame.from_records([info])
    return df

def extract_top_games(i):
    df = pd.DataFrame()

    URL = f"https://boardgamegeek.com/browse/boardgame/page/{i}"
    page = requests.get(URL, cookies=cookies, headers=headers)
    string = page.text
        
    href = re.findall(r'href=\"\/boardgame(.*?)"', string)
    href = href[::2]

    sum_df = 0
    
    try:
        con = 0
        for h in href:
            con +=1
            print(h)
            URL = f'https://boardgamegeek.com/boardgame{h}'
            info = parse_game(URL)
            info['link'] = URL
            sum_df.append(info)
            # if con == 3:
            #     break
       
        df = pd.concat(sum_df)
    except:
        pass

    return df

# x = extract_top_games(1001)

df = pd.DataFrame()
for i in range(1,1001):
    print('-------------------------', i, '-------------------------')
    games = extract_top_games(i)
    df = pd.concat([df, games])

import pandas as pd

csvfile = 'C:\Users\kosti\Documents\NLP\913_Dialogue_Systems\boardbot\games_db_1000.csv'
    
# df.to_csv(csvfile, index=False)

