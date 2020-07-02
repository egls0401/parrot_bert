import os
import argparse
from bell_crawler import BellCrawler
import pdb

def parse_args():
  parser = argparse.ArgumentParser(description="더벨 경제 기사 크롤러")
  parser.add_argument('-n', '--n_process', help='병렬 프로세스 개수', type=int, default=os.cpu_count())
  # parse.add_argument('-c', '--n_code', help='특정 코드', type=str, default=None)

  return parser.parse_args()


def main():
  args = parse_args()
  bell_crawler = BellCrawler(args.n_process)
  bell_crawler.fetch_all()

  # if args.code:
  #   bel_crawler.fetch_one(args.code)
  # else:
  #   bell_crawler.fetch_all()

if __name__ == '__main__':
  main()