import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import openpyxl
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

opts = Options()
opts.add_argument("--log-level=3")
browser = Chrome(executable_path='chromedriver.exe', options=opts)


def download_photos(url, article):
    browser.get(url)
    browser.fullscreen_window()
    soup = bs(browser.page_source, 'html.parser')
    links = [soup.find('a', class_='js__fancybox slick-slide slick-current slick-active')]
    links += soup.findAll('a', class_='js__fancybox slick-slide')
    i = 0
    for l in links:
        try:
            p = requests.get(l.find('img')['src'].replace('/555_455_1', '').replace('/resize_cache', ''))
            if (p.status_code == 200):
                with open('photos/'+article+'_'+str(i)+'.jpg', 'bw') as f:
                    f.write(p.content)
            i += 1
        except Exception:
            try:
                p = requests.get(l.find('img')['data-lazy'].replace('/555_455_1', '').replace('/resize_cache', ''))
                if (p.status_code == 200):
                    with open('photos/'+article+'_'+str(i)+'.jpg', 'bw') as f:
                        f.write(p.content)
                i += 1
            except Exception:
                print(f'Can download photo {i} from article {article}')    
        

if not os.path.isdir('photos'):
    os.mkdir('photos')
    
    
url = 'https://www.kant.ru'

wb = openpyxl.open('buff.xlsx').active
articles = [i.value[:16] for i in wb['A']]


browser.get(url)
browser.fullscreen_window()

for article in articles:
    try:
        sleep(1)
        print(article)
        browser.find_element(By.XPATH, '/html/body/div[4]/div/header[1]/div[2]/div[1]/form/input').send_keys(article, Keys.ENTER)
        download_photos(browser.current_url, article)
    except Exception:
        print(f'No article {article}')

sleep(5)


browser.close()