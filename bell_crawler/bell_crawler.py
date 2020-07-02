import os
import time
import pdb
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import logging
from itertools import repeat
import multiprocessing
from multiprocessing import Pool
# from multiprocessing import Pool, freeze_support

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
BASE_URL = 'https://www.thebell.co.kr'

logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s - %(asctime)s.%(msecs)03d] (%(filename)s:%(lineno)d) > %(message)s',
        datefmt='%Y-%m-%d %H:%M',
    )

logger = logging.getLogger('bell')

class BellCrawler:
  def __init__(self, n_process):
      self.n_process = n_process

  def get_href(self, a_tag):
    full_link = 'https://www.thebell.co.kr/free/content/{}'.format(a_tag['href'])
    return full_link

  def save_as_txt(self, content,i):
        with open('../더벨/bell_{}.txt'.format(i), 'a', encoding='utf-8') as f:

          sentences = re.split(r"(?<=[.!?])\s+", content.strip())
          # 더벨 기사 첫줄은 '이 기사는 2020년 05월 27일 13:31 더벨 유료페이지에 표출된 기사입니다.' 와 같아서 삭제
          sentences = sentences[1:]
          for sentence in sentences:
              sentence = sentence.replace('.', '')
              sentence = sentence.replace('\n', '')
              f.writelines(sentence + "\n")
          f.writelines("\n")

  def get_links(self, page):
    try:
        url = BASE_URL + "/free/content/article.asp?page={}&svccode=00".format(page)
        response = requests.get(url, headers=HEADERS)
    except Exception as e:
        logger.error("{} 응답 에러".format(url))
        logger.error(str(e))
        time.sleep(5)
        pass
    else:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        article_links = soup.select('div.listBox > ul > li > dl > a')
        article_links = list(map(self.get_href, article_links))

    return article_links

  def fetch_by_page(self, link, page):
    try:
        msg = 'cur_page={}'.format(page)
        print(msg, end=len(msg)*'\b', flush=True)
        response = requests.get(link, headers=HEADERS)
    except Exception as e:
        logger.error(str(e))
        time.sleep(5)
        pass
    else:
        try:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            soup = soup.select('#article_main')[0]
            content = soup.getText()
            # logger.info(content)
            index = int(page / 100) + 1 # 100페이지씩 기사 묶음 / 총 140개 정도 나와야함
            self.save_as_txt(content, index)
            logger.info("{} 기사 크롤링 완료".format(link))
        except Exception as e:
            logger.error("{} 기사 크롤링 중 오류 발생".format(link))
            logger.error(str(e))
            pass

  def fetch_all(self):
    # # 더 벨 기사는 13444페이지까지 존재
    for page in range(1, 13444):
        article_links = self.get_links(page)
        # # 아래 코드는 안돌아감
        # poo.map(scraipping, article_links, page)
        start_time = time.time()
        with Pool(processes=self.n_process) as pool:
            pool.starmap(self.fetch_by_page, zip(article_links, repeat(page)))
            print("--- 걸린 시간: %s seconds ---" % (time.time() - start_time))