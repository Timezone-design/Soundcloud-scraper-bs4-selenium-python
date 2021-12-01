import sys
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import json
import requests
from datetime import datetime

from constants import *
from resources import get_endless_scroll_content, check_genre, check_bio, get_genre_excludes, get_genre_includes, get_manager_bio_detect, get_manager_email_detect, get_other_info_of_rapper, generate_password, months, get_LA_includes, get_popularity

RESCRAPE = False

def am_get_email_and_instagram_info_of_rapper(soup):
	email = None
	instagram_username = None
	soundcloud_url = None
	website_url = None

	instagram_username = soup.find('a', class_='social-icon--instagram')['href'].rsplit('/', 1)[1]
	email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', soup.find('div', class_='ArtistHeader-module__bio--siafZ').get_text())
	
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
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for All")
		instawriter.writerow(ALL_FILE_HEADER_AUDIOMACK)
		
	rapper_profile_url = []
	rapper_profile_url_unique = []

	if not os.path.exists("audiomack/rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("audiomack/rappers.txt"): # if not, to see if it can be created from duplicate series
			with open('audiomack/rappers.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('audiomack/rappers_unique.txt', 'w') as f:
				for item in rapper_profile_url_unique:
					url_deletion_flag = False
					for url_deletion_item in url_deletion_list:
						if url_deletion_item in item.strip():
							url_deletion_flag = True
					if url_deletion_flag:
						print(item.strip(), '\tis removed for it has a word in deletion list.')
						continue
					f.write("%s\n" % item.strip())

		else:
			print("Please make audiomack/rappers.txt first!")

	else:
		with open('audiomack/rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item)

	print("{} unique rapper URLs detected.".format(len(rapper_profile_url_unique)))

	driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
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

		driver.get(rapper.strip())
		l = driver.find_element_by_class_name('Button-module__button--2psmQ')
		l.click()
		time.sleep(2)
		rapper_soup = BeautifulSoup(driver.page_source, "html.parser")

		all_genres = rapper_soup.find_all(class_='music-detail__tag')
		all_genres = [x.get_text().strip().replace('#', '') for x in all_genres]
		if not check_genre(all_genres, 2, RESCRAPE):
			print(f'Song genres do not match include list. Passing to next url.')
			continue

		bio = rapper_soup.find('div', class_='ArtistHeader-module__bio--siafZ')
		genre = ''
		role = 'Artist'

		if not bio:
			print("Bio not detected. Passing to next url.")
			continue

		genre = rapper_soup.find('span', class_='ArtistHeader-module__label--2qKDp').find('a').get_text()
		genre_includes = get_genre_includes()
		if not genre in genre_includes:
			print(f'Artist genre {genre} is not in the include list. Passing to next url.')
			continue
		
		if not check_bio(bio):
			print('Bio contains words which are not valid. Passing to next url.')
			continue
		
		bio_text = bio.text
		manager_bio = get_manager_bio_detect()
		for item in manager_bio:
			if item in bio_text:
				role = 'Manager'

		print('Searching {}th user as above url.'.format(rapper_profile_url_unique.index(rapper) + 1))

		rapper_email, rapper_instagram_username, soundcloud_url, website_url = am_get_email_and_instagram_info_of_rapper(rapper_soup)

		if rapper_email or rapper_instagram_username:
			username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull, followers, popularity, songlink = get_other_info_of_rapper(rapper_soup, rapper.strip().split('/')[-1])
			if username == fullname == artistname == artistnamecleaned == location == country == songtitle == songtitlefull == 'excluded':
				print('User info includes exception words. Passing to next url')
				continue
			
			try:
				couponcodename = 'Discount -$30 for mp3 lease for {}'.format(artistnamecleaned)
				couponcode = generate_password(10)
				songplays = rapper_soup.find('li', class_='sc-ministats-item').find(class_='sc-visuallyhidden').text.split()[0].replace(',', '')
				if songplays == "View":
					songplays = "0"
				print('Recent song play: {}'.format(songplays))
				uploaddate = rapper_soup.find(class_='soundTitle__uploadTime').find('time')['datetime'].split('T')[0]
				print('Recent song upload: {}'.format(uploaddate))
				uploaddateobj = datetime.fromisoformat(uploaddate)
				uploadedmonth = months(datetime.today(), uploaddateobj)
				print('Recent song upload was {} months ago'.format(uploadedmonth))
				popularityadjusted = popularity
				if popularity != 'unknown':
					temp = get_popularity(rapper_soup, followers)
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
				print('Error parsing couponcodes and popularity information. Moving to next iteration.')
				continue
				pass
			
			inlosangeles = "No"
			LA_includes = get_LA_includes()
			if location in LA_includes:
				inlosangeles = "Yes"

			if rapper_email:
				manager_email = get_manager_email_detect()
				for item in manager_email:
					if item in rapper_email:
						role = 'Manager'
				has_instagram = 'No'
				if rapper_instagram_username:
					has_instagram = 'Yes'
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus, inlosangeles])

	driver.close()
		

	emailFile.close()
	instaFile.close()

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

	get_rapper_details()




main()
