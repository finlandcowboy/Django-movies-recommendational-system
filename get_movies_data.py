from data_parse import get_proxy
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import proxies
import time
import logging
f = open('movies_url.txt', 'r')
movies_url = f.readlines()

FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(filename='get_movies_data.log', level=logging.DEBUG, format=FORMAT, datefmt='%d/%m/%Y %I:%M:%S %p')



'''

Example: 

'''


def soup_none_log(attribute):
    if attribute is None:
        logging.debug(f'ERROR: Can\'t find movie {attribute}. Url: {url}. Output: {attribute}')


def get_value(attribute):
    return ', '.join([attr.text for attr in attribute])
        



global soup
for url in movies_url:
    for proxy in proxies.proxy_list:
        response = requests.get(url=url)

        if response.status_code != 200:
            logging.debug(f'ERROR: GET \'{url}\' requst code {response.status_code}. Proxy: {proxies.get_proxy(proxy)}')
            time.sleep(0.1)
            continue
        
        soup = BeautifulSoup(response.content, features='lxml')

        if 'робот' in soup.text:
            logging.debug(f'ERROR: Captcha. Proxy: {proxies.get_proxy(proxy)}')
            time.sleep(0.1)
            continue

        name_attr = soup.find_all('span', attrs = {'data-tid': '67e47501'})
        name = get_value(name_attr)
        soup_none_log(name)
        english_name_attr = soup.find_all('span', attrs = {'data-tid': 'e2c7ce8a'})
        english_name = get_value(english_name_attr)
        soup_none_log(english_name)
        year_attr = soup.find_all('a', attrs={'class': 'styles_linkDark__3aytH styles_link__1N3S2'})
        year = get_value(year_attr)
        soup_none_log(english_name)
        countries_attr = soup.find_all('span', attrs = {'data-tid': '60f1c547'})
        countries = get_value(countries_attr)
        soup_none_log(countries)

        
