from itertools import count
import sys
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime

from constants import *
from resources import am_check_additional_genre, get_endless_scroll_content, am_check_genre, check_bio, get_genre_includes, get_manager_bio_detect, get_manager_email_detect, generate_password, months, get_LA_includes, am_get_other_info_of_rapper, am_get_popularity, am_close_ad, text_to_num, am_get_genre_excludes

RESCRAPE = False


def follower_boost(url):
  print('Searching following in \t' + url + '\n')
  with open('audiomack/position_of_rappers_unique_for_following_permalink.txt', 'a', encoding='utf-16') as f:
    f.write("%s\n" % datetime.now())
    f.write("%s\n\n" % url)
  print('Position saved to audiomack/position_of_rappers_unique_for_following_permalink.txt. Now scrolling page...')
  additional_rappers = []

  soup = get_endless_scroll_content(url + '/followers')  

#   next_button_available = True
#   driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
#   driver.get(url)
#   time.sleep(2)
#   driver = am_close_ad(driver)
#   next_button = driver.find_elements(By.CSS_SELECTOR, '[data-direction="next"]')[-1]

#   if not next_button:
#     next_button_available = False

#   count = 0
#   print("Pressing next button...")

#   while next_button_available:
#     actions = ActionChains(driver)
#     actions.move_to_element_with_offset(next_button, 10, 10).pause(1).click().perform()
#     print(str(count), end=' ')
#     count = count + 1
#     # next_button.click()
#     time.sleep(1)
#     next_button = driver.find_elements(By.CSS_SELECTOR, '[data-direction="next"]')[-1]
#     if not next_button or next_button.get_attribute('disabled') != None:
#       next_button_available = False
#   print('')
  try:
    follower_section = soup.select('[class*="ArtistPage-module__section"]')[-1]
  except:
    print("No follower section found.")
    return

  for following_profile in follower_section.find_all('a'):
    additional_rappers.append('https://audiomack.com' + following_profile.attrs['href'])
    print(following_profile.attrs['href'], "\tis added by following boost.")

  with open('audiomack/following_permalink.txt', 'a', encoding='utf-16') as f:
    for item in additional_rappers:
      f.write("%s\n" % item)
  print("\n{} follower urls are added.\n".format(len(additional_rappers)))


def am_get_email_and_instagram_info_of_rapper(soup):
    email = None
    instagram_username = None
    soundcloud_url = None
    website_url = None

    soup = soup.select_one('div[class*="ArtistPage-module__headerWrap"]')

    try:
        instagram_username = soup.select_one('a[class*="social-icon--instagram"]')['href'].split('/')[3]
    except:
        instagram_username = ''

    try:
        email = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', soup.select_one('div[class*="ArtistHeader-module__bio"]').get_text())
    except:
        pass

    # if email:
    #     email = email.group(0)

    soundcloud_url = 'No'

    try:
        website_url = soup.select_one('a[class*="social-icon--url"]')['href']
    except:
        website_url = 'No'

    return email, instagram_username, soundcloud_url, website_url


def get_rapper_details():

    filenameEmail = "audiomack/Rappers with Email.csv"
    filenameInstagram = "audiomack/Rappers with Instagram.csv"
    filenameAll = "audiomack/Rappers All.csv"

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

    rapper_profile_url = []
    rapper_profile_url_unique = []

    # check if unique series of data exists
    if not os.path.exists("audiomack/following_rappers_unique.txt"):

        # if not, to see if it can be created from duplicate series
        if os.path.exists("audiomack/following_permalink.txt"):
            with open('audiomack/following_permalink.txt', encoding='utf-16') as f:
                for item in f:
                    rapper_profile_url.append(item)

            rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
            rapper_profile_url_unique = [i.strip()
                                         for i in rapper_profile_url_unique]

            url_deletion_list = ['beat', 'repost', 'network', 'prod']
            with open('audiomack/following_rappers_unique.txt', 'w', encoding='utf-16') as f:
                for item in rapper_profile_url_unique:
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
            print("Please make audiomack/following_permalink.txt first!")

    else:
        with open('audiomack/following_rappers_unique.txt', encoding='utf-16') as f:
            for item in f:
                rapper_profile_url_unique.append(item)

    print("{} unique rapper URLs detected.".format(
        len(rapper_profile_url_unique)))

    driver = webdriver.Chrome(options=DRIVER_OPTIONS,
                              executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(10000)

    for rapper in rapper_profile_url_unique:

        rapper_email = None
        rapper_instagram_username = None
        rapper_instagram_url = None
        username = None
        fullname = None
        artistname = None
        location = None
        country = None
        songtitlefull = None
        songtitle = None

        print('\n\nRapper url: ', rapper.strip())

        driver.set_page_load_timeout(10)
        try:
            driver.get(rapper.strip())
        except:
            pass
        # Check if ad exists
        driver = am_close_ad(driver)
        try:
            l = driver.find_element(by=By.CSS_SELECTOR, value='[class*="Button-module__button"]')
            l.click()
        except:
            pass
        time.sleep(2)
        rapper_soup = BeautifulSoup(driver.page_source, "html.parser")

        title_checker = False
        all_titles = rapper_soup.select('h3[class*="ArtistPage-module__title"]')
        for title in all_titles:
            # print(title.get_text().strip().lower())
            if "latest" in title.get_text().strip().lower():
                title_checker = True
                break

        if not title_checker:
            print("This guy does not have his tracks. Skipping...")
            continue

        # check if string latest tracks exists
        result = rapper_soup.find_all(text=re.compile("Latest Tracks", re.IGNORECASE))
        print(len(result))

        if len(result) == 0:
            print("Profile is fan/listner. Passing to next url")
            continue

        all_genres = rapper_soup.select('a[class*="MusicTags-module__tag"]')
        all_genres = [x.get_text().strip().replace('#', '')
                      for x in all_genres]
        if not am_check_genre(all_genres, 2, RESCRAPE):
            print(f'Song genres do not match include list. Passing to next url.')
            continue

        bio = rapper_soup.select_one('[class*="ArtistHeader-module__bio"]')
        genre = ''
        role = 'Artist'

        genre_text = ''
        for gen in genre:
            if 'Genre' in gen.get_text():
                genre_text = gen.find('a').get_text()
                break
        genre = genre_text
        genre_excludes = am_get_genre_excludes()
        if genre in genre_excludes:
            print(
                f'Artist genre {genre} is in the audiomack genre exclude list. Passing to next url.')
            continue

        additional_genre = rapper_soup.select('a[class*="MusicTags-module__tag"]')
        if genre == "":
            genre = am_check_additional_genre(additional_genre)

        if bio and not check_bio(bio):
            print('Bio contains words which are not valid. Passing to next url.')
            continue
        
        if bio:
            bio_text = bio.text
            manager_bio = get_manager_bio_detect()
            for item in manager_bio:
                if item in bio_text:
                    role = 'Manager'

        print('Searching {}th user as above url.'.format(
            rapper_profile_url_unique.index(rapper) + 1))

        rapper_email, rapper_instagram_username, soundcloud_url, website_url = am_get_email_and_instagram_info_of_rapper(
            rapper_soup)

        if rapper_email or rapper_instagram_username:
            username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull, followers, popularity, songlink, phoneno1, phoneno2 = am_get_other_info_of_rapper(
                rapper_soup, rapper.strip())
            if username == fullname == artistname == artistnamecleaned == location == country == songtitle == songtitlefull == 'excluded':
                print('User info includes exception words. Passing to next url')
                continue

            try:
                couponcodename = 'Discount -$30 for mp3 lease for {}'.format(
                    fullname)
                couponcode = generate_password(10)
                songplays = rapper_soup.find('div', class_='music-interactions__counts').find(
                    class_='music-interaction__count').text.split()[0].replace(',', '')
                songplays = text_to_num(songplays)
                print('Recent song play: {}'.format(songplays))
                uploaddate = rapper_soup.find(
                    class_='music__meta-released').find('time')['datetime'].split('T')[0]
                print('Recent song upload: {}'.format(uploaddate))
                uploaddateobj = datetime.fromisoformat(uploaddate)
                uploadedmonth = months(datetime.today(), uploaddateobj)
                print('Recent song upload was {} months ago'.format(uploadedmonth))
                popularityadjusted = popularity
                if popularity != 'unknown':
                    temp = am_get_popularity(rapper_soup, followers)
                    if temp == 'fake':
                        popularityadjusted = temp
                activestatus = 'Active'
                if uploadedmonth > 11:
                    activestatus = 'Inactive'
                gostatus = 'No'
                if songlink == 'none':
                    gostatus = 'Yes'
                    songlink = rapper.strip().rsplit('/', 1)[1]

            except:
                print(
                    'Error parsing couponcodes and popularity information. Moving to next iteration.')
                continue
                pass

            inlosangeles = "No"
            LA_includes = get_LA_includes()
            if location in LA_includes:
                inlosangeles = "Yes"

            has_email = 'No'
            has_instagram = 'No'
            if rapper_instagram_username:
                has_instagram = 'Yes'
            if rapper_email:
                rapper_email = rapper_email.group(0)
                has_email = 'Yes'
                manager_email = get_manager_email_detect()
                for item in manager_email:
                    if item in rapper_email:
                        role = 'Manager'
                emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull,
                                     gostatus, 'https://audiomack.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, phoneno1])
                print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle,
                      songtitlefull, gostatus, 'https://audiomack.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, phoneno1])

            if rapper_instagram_username:
                instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus,
                                     'https://audiomack.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, phoneno1])
                print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull,
                      gostatus, 'https://audiomack.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, phoneno1])

            allwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, 'https://audiomack.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles, has_email, soundcloud_url, ('Yes', 'No')[website_url == 'No'], (website_url, '')[website_url == 'No'], phoneno1])

        else:
            print("No email or instagram username found.")

    driver.close()

    emailFile.close()
    instaFile.close()


def get_profile_list():
    # opening the start URL and get profiles
    if os.path.exists('audiomack/rapper.txt'):
        print('rappers.txt exists. Do you want to scrape the audiomack again anyway?')
        append_write = 'a'
    else:
        print('rappers.txt does not exist. Do you want to create it?')
        append_write = 'a'

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
                print(
                    "rappers.txt exists. Moving to next steps to scrape each profiles.")
                pass
            else:
                print("rappers.txt also not found. Terminating the scraper...")
                sys.exit()

        blocks = soup.find_all(class_="music-detail-container")
        for block in blocks:
            href = block.find('ul', class_='music__meta').find(
                'li', class_='music__meta-released').find('a')['href']
            href = 'https://audiomack.com' + href
            with open('audiomack/rapper.txt', append_write, encoding='utf-16') as f:
                f.write(href)
                f.write('\n')
                print(f'{href} is written in rappers.txt')

        print('rappers.txt update finished.')

    print('Now creating rappers_unique.txt')

    rappers = []
    with open('audiomack/rapper.txt', 'r', encoding='utf-16') as f:
        for line in f:
            rappers.append(line.strip())

    rappers_unique = []
    if os.path.exists('audiomack/rappers_unique.txt'):
        with open('audiomack/rappers_unique.txt', 'r', encoding='utf-16') as f:
            for line in f:
                rappers_unique.append(line.strip())

    rappers_list = pd.unique(rappers).tolist()

    with open('audiomack/rappers_unique.txt', 'a', encoding='utf-16') as f:
        for item in rappers_list:
            if not item in rappers_unique:
                f.write(item)
                f.write('\n')

    print('rappers_unique.txt updated.')


def main():
  # get_profile_list()

  if not os.path.exists('audiomack/rappers_unique.txt'):
    print('Please make rappers_unique.txt first. Exiting...')
    sys.exit()
  
  flag = ''
  print('Performing follower boost?')
  while True:
    flag = input("Y or N: ")
    if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
      flag = flag.lower()
      break
    print("Please input Y or N.")
    
  if flag == 'y':
    unique_list = []
    with open('audiomack/rappers_unique.txt', 'r', encoding='utf-16') as f:
      for item in f:
        unique_list.append(item.strip())
    for item in unique_list:
      follower_boost(item)
    
  get_rapper_details()


main()
