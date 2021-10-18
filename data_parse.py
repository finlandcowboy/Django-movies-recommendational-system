from os import error, stat_result
from bs4 import BeautifulSoup
import requests
import proxies

import logging
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='data_parse.log', format=FORMAT, level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S %p')


url = 'https://www.kinopoisk.ru/top/navigator/'
base_url = 'https://www.kinopoisk.ru'


stat = {
    'robot_error' : 0,
    'proxy_connection_error' : 0,
    'kinopoisk_unknown_error' : 0,
    'movie_urls_parsed' : 0,
    'ratings_parsed' : 0
}

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


logging.debug('Start Parsing...')
logging.debug('Opening files...')
movies_url_file = open('movies_url.txt', 'w')
kinopoisk_rating_file = open('kinopoisk_rating.txt', 'w')
logging.debug('Files opened!')
global soup
for page in tqdm(kinopoisk_pages[:5]):
    logging.debug(f'Parsing page: {page}')
    for proxy in proxies.proxy_list:
        #logging.debug(f'Proxy: {proxy}')
        resp = requests.get(page, proxies={'https:':proxies.get_proxy(proxy)})
        if resp.status_code != 200:
            #logging.debug(f'Error GET Code {resp.status_code}')
            time.sleep(0.01)
            stat['proxy_connection_error'] += 1
            continue
        soup = BeautifulSoup(resp.content, features='lxml')
        if 'робот' in soup.text.lower():
            #logging.debug('Captcha Error')
            time.sleep(0.01)
            stat['robot_error'] += 1
            continue
        
        else:
            #logging.debug('Connection succesfull')
            break
    logging.debug(f'Proxy {proxy} got connection')
    movies_div = soup.find('div', id='itemList')
    if movies_div is None:
        error_dict = {
            'text' : soup.text,
            'url' : page
        }
        error_catcher.append(error_dict)
        stat['kinopoisk_unknown_error'] += 1
        continue
    for movie_page in movies_div.find_all('div', attrs={'class': 'item _NO_HIGHLIGHT_'}):
        #movie_urls.append(base_url + movie_page.find_all('a')[0].get('href'))
        #kinopoisk_rating.append(movie_page.find('div', attrs={'numVote ratingGreenBG'}).find('span').text.split()[0])
        movies_url_file.write(base_url + movie_page.find_all('a')[0].get('href') + '\n')
        if movie_page.find_all('a')[0].get('href'):
            stat['movie_urls_parsed'] += 1
        kinopoisk_rating_file.write(movie_page.find('div', attrs={'numVote ratingGreenBG'}).find('span').text.split()[0]+ '\n')
        if movie_page.find('div', attrs={'numVote ratingGreenBG'}).find('span').text.split()[0]:
            stat['ratings_parsed'] += 1
    logging.debug('Page succesfully parsed')

logging.debug('Parsing succesfully complete!')

for metric in stat:
    logging.debug(f'{metric}: {stat[metric]}')

with open('error.log', 'w') as out:
    for error_dict in error_catcher:
        for key in error_dict:
            out.write(f'{key}: {error_dict[key]}')
            out.write('\n')
        out.write('\n')

