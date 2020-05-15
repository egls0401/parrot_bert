from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time
import pdb
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
options.add_argument('headless') # headless 모드 설정
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

"""
nohup으로 코드를 돌려보자
nohup sh -c "python hankyung_economy_crawling.py" > hankyung.log &
"""

# 속도 향상을 위한 옵션 해제
prefs = {
  'profile.default_content_setting_values': {
    'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2
  }
}
options.add_experimental_option('prefs', prefs)

# 크롬 드라이버 경로 주의
path = '/Users/chanha/Desktop/머신러닝/chromedriver_81'

# User-Agent는 https://www.whatismybrowser.com/detect/what-is-my-user-agent 여기서 찾을 수 있음
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

def scrapping():
    driver = webdriver.Chrome(path, options=options)
    driver.maximize_window()

    def get_href(a_tag):
        return a_tag.get_attribute('href')

    def save_as_txt(content,i):
        with open('한경/hankyung_articles_{}.txt'.format(i), 'a', encoding='utf-8') as f:
            sentences = re.split("(?<=[.!?])\s+", content.strip())
            sentences = sentences[:-1] # 마지막은 보통 기자 이름이라 뺌
            for sentence in sentences:
                sentence = sentence.replace('.', '')
                sentence = sentence.replace('\n', '')
                f.writelines(sentence + "\n")
                print(sentence)
            f.writelines("\n")

    for i in range(3100, 14273):
        article_links = []

        try:
            driver.get(
                "https://www.hankyung.com/economy?hkonly=true&page={}".format(i)
            )
        except:
            print('driver open 실패')
            time.sleep(5)
            continue
        else:
            print("{}페이지 크롤링 중...".format(i))
            article_links = driver.find_elements_by_css_selector('ul.list_basic > li > div.article > h3 > a')
            article_links = list(map(get_href, article_links))
            # driver.quit()

        for link in article_links:
            try:
                response = requests.get(link, headers=headers)
            except requests.ConnectionError as e:
                print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
                print(str(e))
                time.sleep(10)
                continue
            except requests.Timeout as e:
                print("OOPS!! Timeout Error")
                print(str(e))
                time.sleep(10)
                continue
            except requests.RequestException as e:
                print("OOPS!! General Error")
                print(str(e))
                time.sleep(10)
                continue
            except:
            # except KeyboardInterrupt:
                time.sleep(10)
                continue
            else:
                try:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    soup = soup.select('#articletxt')[0]
                    content = soup.getText()
                    index = int(i / 100) + 1 # 100페이지씩 기사 묶음 / 총 140개 정도 나와야함
                    save_as_txt(content, index)
                except:
                    print('오류발생')
                    continue

if __name__ == '__main__':
    scrapping()