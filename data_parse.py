from os import error
from bs4 import BeautifulSoup
import requests


proxies = [
    {
        'ip' : '190.107.224.150',
        'port' : 3128
    },
    {
        'ip' : '79.160.233.21',
        'port' : 8118
    },
    {
        'ip' : '51.83.69.9',
        'port' : 8118
    },
    {
        'ip' : '185.216.231.13',
        'port' : 8888
    },
    {
        'ip' : '52.183.8.192',
        'port' : 3128
    },
    {
        'ip' : '31.148.96.50',
        'port' : 3128
    },
    {
        'ip' : '167.114.96.27',
        'port' : 9300
    }
]


url = 'https://www.kinopoisk.ru/top/navigator/'
base_url = 'https://www.kinopoisk.ru'

'''

Movie data example

movie_data = {
    'name' : 'string',
    'kinopoisk_rating' : 'float',
    'year' : 'string',
    'country' : 'string',
    'director' : 'string',
    'genre' : 'string',
    'actors': 'list',
    'poster' : 'url to image',
    'description' : 'string',
    'world_premiere' : 'date',
    'budget' : 'int',
    'fees_in_usa' : 'int',
    'fees_in_world' : 'int'
} 
'''
data = []
kinopoisk_rating = []

kinopoisk_pages = [f'https://www.kinopoisk.ru/top/navigator/m_act[num_vote]/100/m_act[rating]/1%3A/order/rating/page/{i}/#results' for i in range(1,1327)]


error_catcher = []

from tqdm import tqdm
import time
tryies = 10
movie_urls = []

def get_proxy(proxy):
    return f"https://{proxy['ip']}:{proxy['port']}"

global soup
for page in tqdm(kinopoisk_pages):
    for proxy in proxies:
        #print(f'Proxy: {proxy}')
        resp = requests.get(page, proxies={'https:':get_proxy(proxy)})
        if resp.status_code != 200:
            #print(f'Error GET Code {resp.status_code}')
            time.sleep(2)
            continue
        soup = BeautifulSoup(resp.content, features='lxml')
        if 'робот' in soup.text:
            #print('Captcha Error')
            time.sleep(2)
            continue
        
        else:
            #print('Connection succesfull')
            break

    movies_div = soup.find('div', id='itemList')
    if movies_div is None:
        error_dict = {
            'text' : soup.text,
            'url' : page
        }
        error_catcher.append(error_dict)
        continue
    for movie_page in movies_div.find_all('div', attrs={'class': 'item _NO_HIGHLIGHT_'}):
        movie_urls.append(base_url + movie_page.find_all('a')[0].get('href'))
        kinopoisk_rating.append(movie_page.find('div', attrs={'numVote ratingGreenBG'}).find('span').text.split()[0])
        
print(len(movie_urls))
print(len(kinopoisk_rating))

with(open('movies_url.txt'), 'w') as out:
    for url in movie_urls:
        out.write(f'{url}\n')

with(open('kinopoisk_rating.txt'), 'w') as out:
    for rating in kinopoisk_rating:
        out.write(f'{rating}\n')

with(open('error_log.txt'), 'w') as out:
    for error in error_catcher:
        out.write(f"Text: {error['text']}\nPage: {error['page']}\n\n")

