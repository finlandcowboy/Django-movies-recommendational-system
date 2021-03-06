import requests
from bs4 import BeautifulSoup
import time 
import proxies
import random
from tqdm import tqmd
movie_end_url = []
error_count = 0
proxy_list = proxies.proxy_list
for page in tqdm(range(5), desc='Page'):
    time.sleep(random.randint(0,10) * error_count)
    for proxy in tqdm(proxy_list, desc='Proxy'):
        url = f'https://www.kinopoisk.ru/lists/top250/?page={page+1}&tab=all'
        print(url)
        resp = requests.get(url, proxies={'https:':proxies.get_proxy(proxy)})
        soup = BeautifulSoup(resp.content, 'lxml')

        if 'отправляли' in soup.text:
            error_count += 1
            time.sleep(1 * (1.05**error_count))
            proxy_list.remove(proxy)
            continue
        
        if not soup.find('div', attrs={'class': 'selection-list'}):
            error_count += 1
            time.sleep(1 * (1.05**error_count))
            proxy_list.remove(proxy)
            continue

        print(soup.text)
        for movie in soup.find('div', attrs={'class': 'selection-list'}).find_all('div', attrs={'class': 'desktop-rating-selection-film-item__content-wrapper'}):
            movie_end_url.append(movie.find('a').get('href'))
        

with open('top250.txt', 'w') as file:
    for url in movie_end_url:
        file.write('https://kinopoisk.ru' + url)
        file.write('\n')