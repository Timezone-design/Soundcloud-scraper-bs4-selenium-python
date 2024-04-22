import os
import string
import sys
import pandas as pd

from constants import BEATSTARS_SEARCH_URL
from resources import get_endless_scroll_content

def get_profile_list():
    # opening the start URL and get profiles
    if os.path.exists('beatstars/beatmakers.txt'):
        print('beatmakers.txt exists. Do you want to scrape the beatstars and add the beatmakers anyway?')
        append_write = 'a'
    else:
        print('beatmakers.txt does not exist. Do you want to create it?')
        append_write = 'a'
    
    while True:
        flag = input("Y or N: ")
        if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
            flag = flag.lower()
            break
        print("Please input Y or N.")

    if flag == 'n':
        return

    try:
        for char in list(string.ascii_lowercase):
            soup = get_endless_scroll_content(BEATSTARS_SEARCH_URL + char)
            blocks = soup.find_all('mp-card-figure-member')
            for block in blocks:
                swiper = block.find('mp-swiper-list-template')
                if swiper.find('article') is None:
                    print(f'\tNo tracks found. Skipping...')
                button = block.find('div', class_='more-options')
                if button.find('a') is None:
                    continue
                href = button.find('a')['href']
                href = f'https://beatstars.com{href}'
                with open('beatstars/beatmakers.txt', append_write, encoding='utf-8') as f:
                    f.write(href)
                    f.write('\n')
                    print(f'{href} is written in beatmakers.txt')

    except Exception as e:
        print(e)
        print('Error occurred while scrolling content.')
        if os.path.exists('beatstars/beatmakers.txt'):
            print(
                "beatmakers.txt exists. Moving to next steps to scrape each profiles.")
            pass
        else:
            print("beatmakers.txt also not found. Terminating the scraper...")
            sys.exit()

    print('Creating beatmaker_unique.txt')

    beatmakers = []
    with open('beatstars/beatmakers.txt', 'r', encoding='utf-8') as f:
        for line in f:
            beatmakers.append(line.strip())

    beatmakers_unique = []
    if os.path.exists('beatstars/beatmakers_unique.txt'):
        with open('beatstars/beatmakers_unique.txt', 'r', encoding='utf-8') as f:
            for line in f:
                beatmakers_unique.append(line.strip())

    beatmakers_list = pd.unique(beatmakers).tolist()

    with open('beatstars/beatmakers_unique.txt', 'a', encoding='utf-8') as f:
        for item in beatmakers_list:
            if not item in beatmakers_list:
                f.write(item)
                f.write('\n')

    print('beatmakers_unique.txt updated.')


def main():
    get_profile_list()
    # get_beatmaker_details()

main()