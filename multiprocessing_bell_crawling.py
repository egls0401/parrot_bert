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
import logging
from itertools import repeat
from multiprocessing import Pool, freeze_support

"""
nohup으로 코드를 돌려보자
nohup sh -c "python bell_economy_crawling.py" > bell.log &
"""

headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

def get_href(a_tag):
    full_link = 'https://www.thebell.co.kr/free/content/{}'.format(a_tag['href'])
    return full_link

def save_as_txt(content,i):
        with open('더벨/bell_{}.txt'.format(i), 'a', encoding='utf-8') as f:
          sentences = re.split(r"(?<=[.!?])\s+", content.strip())
          # 더벨 기사 첫줄은 '이 기사는 2020년 05월 27일 13:31 더벨 유료페이지에 표출된 기사입니다.' 와 같아서 삭제
          sentences = sentences[1:]
          for sentence in sentences:
              sentence = sentence.replace('.', '')
              sentence = sentence.replace('\n', '')
              f.writelines(sentence + "\n")
          f.writelines("\n")

def get_links(page):
    try:
        url = "https://www.thebell.co.kr/free/content/article.asp?page={}&svccode=00".format(page)
        response = requests.get(url, headers=headers)
    except Exception as e:
        logger.error("{} 응답 에러".format(url))
        logger.error(str(e))
        time.sleep(5)
        pass
    else:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        article_links = soup.select('div.listBox > ul > li > dl > a')
        article_links = list(map(get_href, article_links))

    return article_links

def scrapping(link, page):
    try:
        response = requests.get(link, headers=headers)
    except Exception as e:
        logger.error(str(e))
        time.sleep(5)
        pass
    else:
        try:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            soup = soup.select('#article_main')[0]
            content = soup.getText()
            # logger.info(content)
            index = int(page / 100) + 1 # 100페이지씩 기사 묶음 / 총 140개 정도 나와야함
            save_as_txt(content, index)
            logger.info("{} 기사 크롤링 완료".format(link))
        except Exception as e:
            logger.error("{} 기사 크롤링 중 오류 발생".format(link))
            logger.error(str(e))
            pass

def main():
    for page in range(1, 3):
        article_links = get_links(page)
        with Pool(processes=4) as pool:
            pool.starmap(scrapping, zip(article_links, repeat(page)))

if __name__ == '__main__':
    """
    - 로그 레벨: CRITICAL(50), ERROR(40), WARNING(3), INFO(20), DEBUG(10), NOTSET(0)
    """
    ## 로그 기본설정
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s - %(asctime)s.%(msecs)03d] (%(filename)s:%(lineno)d) > %(message)s',
        datefmt='%Y-%m-%d %H:%M',
    )

    logger = logging.getLogger('bell')

    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))