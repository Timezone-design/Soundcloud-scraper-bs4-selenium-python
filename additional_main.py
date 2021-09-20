import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import sys
from datetime import datetime
from constants import *
from resources import get_genre_includes, get_bio_excludes, get_manager_bio_detect, generate_password, get_manager_email_detect, get_popularity, months, get_email_and_instagram_info_of_rapper, get_other_info_of_rapper

	
def generate_2nd_permalinks(url):
	url = url + '/likes'
	tempdriver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	tempdriver.set_page_load_timeout(10000)
	tempdriver.get(url)
	time.sleep(1)
	scroll_threshold = 500
	scroll_pause_time = 2
	genre_includes = get_genre_includes()
	print("Following genre will be included.")
	print(genre_includes)

	additional_rappers = []
	i = 0
	with open('position_of_rappers_unique_for_additional_permalink.txt', 'a') as f:
		f.write("%s\n" % datetime.now())
		f.write("%s\n\n" % url)
	print('Position saved to position_of_rappers_unique_for_additional_permalink.txt. Now scrolling page...')
	while True:
		i += 1
		try:
			last_height = tempdriver.execute_script("return document.body.scrollHeight")
			tempdriver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			time.sleep(scroll_pause_time)
			new_height = tempdriver.execute_script("return document.body.scrollHeight")
			print('{}th scroll made.'.format(i))
		except:
			print("error in getting data. Passing to next iteration 12")
			return

		if last_height == new_height or i == scroll_threshold:
			print("Scroll finished. Now scraping... 12")			
			break

	soup = BeautifulSoup(tempdriver.page_source, "html.parser")
	for rapper_profile in soup.find_all(class_="sound__header"):
		for include in genre_includes:
			if rapper_profile.find(class_='sc-tagContent') and include in rapper_profile.find(class_='sc-tagContent').get_text():
				rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
				additional_rappers.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
				print(rapper_profile_url.attrs['href'], "\tis added with genre\t", include, " to additional permalink.txt")
				break

	with open('additional_permalink.txt', 'a') as additional_file:
		for item in additional_rappers:
			additional_file.write("%s\n" % item)
	print("\n{} additional repost urls are added.\n".format(len(additional_rappers)))
	tempdriver.close()


def get_rapper_profile_urls_from_reposts(permalinks):

	scroll_threshold = 10
	while True: # Gets user input for API connection quantity
		scroll_threshold = input("How many scrolls do you want to make for one page? (Default: 10) ")

		try:
			int(scroll_threshold) > 0
			break
		except Exception as e:
			print("Please input a valid integer.")
		else:
			pass
		finally:
			pass

	scroll_threshold = int(scroll_threshold)
	permalinks = pd.unique(permalinks).tolist()
	permalinks = [i.strip() for i in permalinks]

	genre_includes = get_genre_includes()
	print("Following genre will be included.")
	print(genre_includes)
	for permalink in permalinks:
		try:
			driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
			rapper_urls = []
			driver.set_page_load_timeout(10000)
			driver.get(permalink + '/likes')
			time.sleep(2)
			scroll_pause_time = 2
			# scroll_threshold = 10
			i = 0
			print('Now scrolling page...')
			while True:
				i += 1
				last_height = driver.execute_script("return document.body.scrollHeight")
				driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
				time.sleep(scroll_pause_time)
				new_height = driver.execute_script("return document.body.scrollHeight")
				print('{}th scroll made.'.format(i))

				if last_height == new_height or i == scroll_threshold:
					print("Scroll finished. Now scraping... 22")			
					break

			soup = BeautifulSoup(driver.page_source, "html.parser")

			for rapper_profile in soup.find_all(class_="sound__header"):
				for include in genre_includes:
					if rapper_profile.find(class_='sc-tagContent') and include in rapper_profile.find(class_='sc-tagContent').get_text():
						rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
						rapper_urls.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
						print(rapper_profile_url.attrs['href'], "\tis added with genre\t", include)
						break

			driver.close()
			print("\n{} / {} repost urls are searched.\n".format(permalinks.index(permalink) + 1, len(permalinks)))

			with open('additional_rappers.txt', 'a') as f:
				for item in rapper_urls:
					f.write("%s\n" % item)

			print("{} rapper profile URLs are written into file additional_rappers.txt.".format(len(rapper_urls)))
		except:
			driver.close()
			return

	
def get_rapper_details():

	filenameEmail = "Rappers with Email updated.csv"
	filenameInstagram = "Rappers with Instagram updated.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])

	rapper_profile_url = []
	rapper_profile_url_unique = []

	if not os.path.exists("additional_rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("additional_rappers.txt"): # if not, to see if it can be created from duplicate series
			with open('additional_rappers.txt') as f:
				for item in f:
					rapper_profile_url.append(item)
			with open('additional_permalink.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('additional_rappers_unique.txt', 'w') as f:
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
			print("Please make additional_rappers.txt first!")
			sys.exit()

	else:
		with open('additional_rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item)

	print("{} unique rapper URLs detected.".format(len(rapper_profile_url_unique)))

	driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	driver.set_page_load_timeout(10000)

	rappers_before = []
	with open('rappers_unique.txt', 'r') as f:
		for item in f:
			rappers_before.append(item.strip())

	for rapper in rapper_profile_url_unique:
		if rapper.strip() in rappers_before:
			print(rapper.strip() + "/tracks is excluded for it is already scanned in rappers_unique.txt.")
			continue
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

		print('\n\nRapper url: ', rapper.strip() + "/tracks")

		driver.get(rapper.strip() + "/tracks")
		time.sleep(2)
		rapper_soup = BeautifulSoup(driver.page_source, "html.parser")
		bio = rapper_soup.find('div', class_='truncatedUserDescription__content')
		genre = ''
		role = 'Artist'


		if not bio:
			print(rapper.strip() + "/tracks is excluded for there are no bio data.")
			continue
		if rapper_soup.find(class_='sc-tagContent'):
			genre = rapper_soup.find(class_='sc-tagContent').get_text()
		bio_excludes = get_bio_excludes()
		bio_text = bio.text

		flag = 0
		for item in bio_excludes:
			if item in bio_text:
				flag = 1
				break
		if flag == 1:
			print('Bio includes exception word. Passing to next url.')
			continue
		
		manager_bio = get_manager_bio_detect()
		for item in manager_bio:
			if item in bio_text:
				role = 'Manager'

		web_profiles = rapper_soup.find('div', class_="web-profiles")

		print('Searching {}th user as above url.'.format(rapper_profile_url_unique.index(rapper) + 1))

		rapper_email, rapper_instagram_username, rapper_instagram_url = get_email_and_instagram_info_of_rapper(bio, web_profiles)

		if rapper_email or rapper_instagram_username:
			username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull, followers, popularity = get_other_info_of_rapper(rapper_soup, rapper.strip().split('/')[-1])
			if username == fullname == artistname == artistnamecleaned == location == country == songtitle == songtitlefull == 'excluded':
				print(rapper.strip() + "/tracks is excluded for its artist or track data is not matching.")
				continue
			
			couponcodename = 'Discount -$30 for mp3 lease for {}'.format(artistnamecleaned)
			couponcode = generate_password(10)
			songplays = rapper_soup.find('li', class_='sc-ministats-item').find(class_='sc-visuallyhidden').text.split()[0].replace(',', '')
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
				
			if rapper_email:
				manager_email = get_manager_email_detect()
				for item in manager_email:
					if item in rapper_email:
						role = 'Manager'
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])

	driver.close()
		

	emailFile.close()
	instaFile.close()


def main(): # Main workflow of SoundCloud Scraper

	permalinks = []

	if not os.path.exists("additional_permalink.txt"): # Searches if permalinks to repost profiles are already made
		print("additional_permalink not exist!")
		unique_list = []
		with open('rappers_unique.txt', 'r') as f:
			for item in f:
				unique_list.append(item.strip())
		for item in unique_list:
			generate_2nd_permalinks(item)
	else: # If permalinks are already existing in file
		with open('additional_permalink.txt') as f:
			for item in f:
				permalinks.append(item)

	if os.path.exists("rappers_unique.txt"):
		print("It seems there are rappers_unique.txt in your folder. Do you want to make a search in their /likes to add more results?")
		flag = ''
		while True:
			flag = input("Y or N: ")
			if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
				flag = flag.lower()
				break
			print("Please input Y or N.")
		if flag == 'y':
			unique_list = []
			with open('rappers_unique.txt', 'r') as f:
				for item in f:
					unique_list.append(item.strip())
			for item in unique_list:
				generate_2nd_permalinks(item)

	if not os.path.exists("additional_rappers.txt"): # If rappers' profile urls are not scraped from repost profiles
		get_rapper_profile_urls_from_reposts(permalinks)

	print("\n\nOpening additional repost profiles to get rappers...")

	get_rapper_details()

	




main()
		