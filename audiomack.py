import sys
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import json
import requests

from constants import *
from resources import get_endless_scroll_content


def get_profile_list():
  # opening the start URL and get profiles
  if os.path.exists('audiomack/rapper.txt'):
    print('rappers.txt exists. Do you want to scrape the audiomack again anyway?')

  while True:
    flag = input("Y or N: ")
    if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
      flag = flag.lower()
      break
    print("Please input Y or N.")
  if flag == 'y':
    try:
      soup = get_endless_scroll_content(AUDIOMACK_INIT_URL)
    except:
      print('Error occured while scrolling the content.')
      if os.path.exists('audiomack/rapper.txt'):
        print("rappers.txt exists. Moving to next steps to scrape each profiles.")
        pass
      else:
        print("rappers.txt also not found. Terminating the scraper...")
        sys.exit()
    
    blocks = soup.find_all(class_="music-detail-container")
    for block in blocks:
      print(block.prettify())
      href = block.find('ul', class_='music__meta').find('li', class_='music__meta-released').find('a')['href']
      href = 'https://audiomack.com' + href
      with open('audiomack/rapper.txt', 'a', encoding='utf-8') as f:
        f.write(href)
        f.write('\n')
        print(f'{href} is written in rappers.txt')

    print('rappers.txt update finished.')
  
  print('Now creating rappers_unique.txt')

  rappers = []
  with open('audiomack/rapper.txt', 'r', encoding='utf-8') as f:
    for line in f:
      rappers.append(line.strip())

  rappers_unique = []
  if os.path.exists('audiomack/rapper_unique.txt'):
    with open('audiomack/rapper_unique.txt', 'r', encoding='utf-8') as f:
      for line in f:
        rappers_unique.append(line.strip())
  
  rappers_list = pd.unique(rappers).tolist()

  with open('audiomack/rappers_unique.txt', 'a', encoding='utf-8') as f:
    for item in rappers_list:
      if not item in rappers_unique:
        f.write(item)
        f.write('\n')

  print('rappers_unique.txt updated.')


def main():
  
  get_profile_list()

  




main()
