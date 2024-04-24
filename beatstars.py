import os
import re
import string
import sys
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from constants import ALL_FILE_HEADER_AUDIOMACK, BEATSTARS_SEARCH_URL, DRIVER_OPTIONS, DRIVER_PATH, EMAIL_FILE_HEADER_AUDIOMACK, INSTA_FILE_HEADER_AUDIOMACK
from resources import am_close_ad, generate_password, get_LA_includes, get_endless_scroll_content


def get_beatstar_instagram_url(soup):
    links = soup.find_all('a')
    instagram_username = ''
    instagram_url = ''
    for link in links:
        href = link['href']
        if 'instagram' in href:
            instagram_url = href
            instagram_username = href.split('/')[-1]
            break
    return instagram_username, instagram_url


def get_beatstar_email(soup):
    email = ''
    try:
        email = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', soup.get_text())
    except:
        pass
    return email


def get_beatstar_first_song_link(soup):
    url = ''
    title = ''
    if soup is not None:
        links = soup.find_all('a', class_='name')
        for link in links:
            if link['href'][:3] == '/TK':
                url = link['href']
                title = link.text
                break
    return title, url


def get_beatmaker_details():
    filenameEmail = "beatstars/Beatmakers with Email.csv"
    filenameInstagram = "beatstars/Beatmakers with Instagram.csv"
    filenameAll = "beatstars/Beatmakers All.csv"

    emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
    instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')
    allFile = open(filenameAll, 'a', newline='', encoding='utf-16')

    emailwriter = csv.writer(emailFile, delimiter='\t')
    instawriter = csv.writer(instaFile, delimiter='\t')
    allwriter = csv.writer(allFile, delimiter='\t')

    if os.path.getsize(filenameEmail) == 0:
        print("Writing a new file for Email")
        emailwriter.writerow(EMAIL_FILE_HEADER_AUDIOMACK)
    if os.path.getsize(filenameInstagram) == 0:
        print("Writing a new file for Instagram")
        instawriter.writerow(INSTA_FILE_HEADER_AUDIOMACK)
    if os.path.getsize(filenameAll) == 0:
        print("Writing a new file for All")
        allwriter.writerow(ALL_FILE_HEADER_AUDIOMACK)

    beatstar_profile_url = []
    beatstar_profile_url_unique = []


    if not os.path.exists("beatstars/beatmakers_unique.txt"):

        # if not, to see if it can be created from duplicate series
        if os.path.exists("beatstars/beatmakers.txt"):
            with open('beatstars/beatmakers.txt') as f:
                for item in f:
                    beatstar_profile_url.append(item)

            beatstar_profile_url_unique = pd.unique(beatstar_profile_url).tolist()
            beatstar_profile_url_unique = [i.strip()
                                         for i in beatstar_profile_url_unique]

            url_deletion_list = ['beat', 'repost', 'network', 'prod']
            with open('beatstars/beatmakers_unique.txt', 'w') as f:
                for item in beatstar_profile_url_unique:
                    url_deletion_flag = False
                    for url_deletion_item in url_deletion_list:
                        if url_deletion_item in item.strip():
                            url_deletion_flag = True
                    if url_deletion_flag:
                        print(
                            item.strip(), '\tis removed for it has a word in deletion list.')
                        continue
                    f.write("%s\n" % item.strip())

        else:
            print("Please make beatstars/beatmakers.txt first!")

    else:
        with open('beatstars/beatmakers_unique.txt') as f:
            for item in f:
                beatstar_profile_url_unique.append(item)
    
    print("{} unique beatstar URLs detected.".format(
        len(beatstar_profile_url_unique)))
    
    service = webdriver.chrome.service.Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(options=DRIVER_OPTIONS,
                              service=service)
    driver.set_script_timeout(10000)
    driver.set_page_load_timeout(10000)

    for beatstar in beatstar_profile_url_unique:
        beatstar_email = None
        beatstar_instagram_username = None
        beatstar_instagram_url = None
        username = None
        fullname = None
        artistname = None
        location = None
        country = None
        songtitlefull = None
        songtitle = None

        print('\nStar url: ', beatstar.strip())

        try:
            driver.get(beatstar.strip() + '/about')
        except:
            pass

        # Check if ad exists
        driver = am_close_ad(driver)
        try:
            l = driver.find_element_by_id('onetrust-accept-btn-handler')
            l.click()
        except:
            pass
        time.sleep(2)
        username = driver.current_url.split('/')[-1]
        driver.get(driver.current_url + '/about')

        beatstar_soup = BeautifulSoup(driver.page_source, "html.parser")
        about_me_info = beatstar_soup.find('div', class_='about-me-info')
        user_location = beatstar_soup.find('bs-caption-figure-template', class_='user_location')
        if user_location is not None:
            location = user_location.text
        social_network_list = beatstar_soup.find('ul', class_='social-networks-list')
        fullname_soup = beatstar_soup.find('bs-caption-figure-template', class_='s-line heading-s center')
        if fullname_soup:
            fullname = fullname_soup.find('h1').text
        else:
            print("Profile not found, continuing loop.")
        artistname = fullname
        artistnamecleaned = fullname
        
        if about_me_info is not None:
            beatstar_email = get_beatstar_email(about_me_info)
        if social_network_list is not None:
            beatstar_instagram_username, beatstar_instagram_url = get_beatstar_instagram_url(social_network_list)

        if beatstar_email or beatstar_instagram_username:
            couponcodename = 'Discount -$30 for mp3 lease for {}'.format(
                    fullname)
            couponcode = generate_password(10)
            songplays = 0
            uploaddate = ''
            popularity = 'True'
            popularityadjusted = 'True'
            activestatus = 'Active'
            gostatus = 'No'
            songtitle, songlink = get_beatstar_first_song_link(beatstar_soup.find('div', class_='content-media'))
            songtitlefull = songtitle
            inlosangeles = "No"
            LA_includes = get_LA_includes()
            if location in LA_includes:
                inlosangeles = "Yes"
            
            has_email = 'No'
            has_instagram = 'No'
            if beatstar_instagram_url:
                has_instagram = 'Yes'

            if beatstar_email:
                beatstar_email = beatstar_email.group(0)
                emailwriter.writerow([beatstar.strip(), username, fullname, artistname, artistnamecleaned, location, country, beatstar_email, beatstar_instagram_username, beatstar_instagram_url, has_instagram, songtitle, songtitlefull,
                                     gostatus, songlink, '', '', '', popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, ''])

            if beatstar_instagram_url:
                instawriter.writerow([beatstar.strip(), username, fullname, artistname, artistnamecleaned, location, country, beatstar_instagram_username, beatstar_instagram_url, songtitle, songtitlefull, gostatus,
                                     songlink, '', '', '', popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, ''])

            allwriter.writerow([beatstar.strip(), username, fullname, artistname, artistnamecleaned, location, country, beatstar_email, beatstar_instagram_username, beatstar_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, songlink, '', '', '', popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, has_email, '', '', '', ''])
        else:
            print("No email or instagram username found.")

    driver.close()

    emailFile.close()
    instaFile.close()


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

    if flag == 'y':

        try:
            for char in ['a', 'b']:
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
            if not item in beatmakers_unique:
                f.write(item)
                f.write('\n')

    print('beatmakers_unique.txt updated.')


def main():
    get_profile_list()
    get_beatmaker_details()

main()