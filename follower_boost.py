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

	
def generate_follower_permalinks(url):
	url = url + '/following'
	tempdriver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	tempdriver.set_page_load_timeout(10000)
	tempdriver.get(url)
	time.sleep(1)
	scroll_threshold = 500
	scroll_pause_time = 2
	# genre_includes = get_genre_includes()
	# print("Following genre will be included.")
	# print(genre_includes)

	additional_rappers = []
	i = 0
	print('Searching following in \t' + url + '\n')
	with open('follower_boost_txt/position_of_rappers_unique_for_following_permalink.txt', 'a') as f:
		f.write("%s\n" % datetime.now())
		f.write("%s\n\n" % url)
	print('Position saved to follower_boost_txt/position_of_rappers_unique_for_following_permalink.txt. Now scrolling page...')
	while True:
		i += 1
		try:
			last_height = tempdriver.execute_script("return document.body.scrollHeight")
			tempdriver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			time.sleep(scroll_pause_time)
			new_height = tempdriver.execute_script("return document.body.scrollHeight")
			print('{}th scroll made.'.format(i))
		except:
			print("error in getting data. Passing to next iteration 3")
			return

		if last_height == new_height or i == scroll_threshold:
			print("Scroll finished. Now scraping... 12")			
			break

	soup = BeautifulSoup(tempdriver.page_source, "html.parser")

	for following_profile in soup.find_all(class_="userBadgeListItem__image"):
		additional_rappers.append('https://soundcloud.com' + following_profile.attrs['href'])
		print(following_profile.attrs['href'], "\tis added by following boost.")

	with open('follower_boost_txt/following_permalink.txt', 'a') as f:
		for item in additional_rappers:
			f.write("%s\n" % item)
	print("\n{} follower urls are added.\n".format(len(additional_rappers)))

	tempdriver.close()


def get_rapper_details():

	filenameEmail = "csv/Rappers with Email updated.csv"
	filenameInstagram = "csv/Rappers with Instagram updated.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])

	rapper_profile_url = []
	rapper_profile_url_unique = []

	if not os.path.exists("follower_boost_txt/following_rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("follower_boost_txt/following_permalink.txt"): # if not, to see if it can be created from duplicate series
			with open('follower_boost_txt/following_permalink.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('follower_boost_txt/following_rappers_unique.txt', 'w') as f:
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
			print("Please make follower_boost_txt/following_permalink.txt first!")
			sys.exit()

	else:
		with open('follower_boost_txt/following_rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item)

	print("{} unique rapper URLs detected.".format(len(rapper_profile_url_unique)))

	driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	driver.set_page_load_timeout(10000)

	rappers_before = []
	with open('main_txt/rappers_unique.txt', 'r') as f:
		for item in f:
			rappers_before.append(item.strip())

	for rapper in rapper_profile_url_unique:
		if rapper.strip() in rappers_before:
			print(rapper.strip() + "/tracks is excluded for it is already scanned in main_txt/rappers_unique.txt.")
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

		genre_flag = 0
		if rapper_soup.find(class_='sc-tagContent'):
			genre_includes = get_genre_includes()
			genre_first = rapper_soup.find(class_='sc-tagContent').get_text()

			for item in genre_includes:
				if item in genre_first:
					genre_flag = 1
					break
			
		if genre_flag == 0:
			print(rapper.strip() + "/tracks is excluded for its genre is not matching.")
			continue


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
			username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull, followers, popularity, songlink = get_other_info_of_rapper(rapper_soup, rapper.strip().split('/')[-1])
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
			gostatus = 'No'
			if songlink == 'none':
				gostatus = 'Yes'
				songlink = rapper.strip()
				
			if rapper_email:
				manager_email = get_manager_email_detect()
				for item in manager_email:
					if item in rapper_email:
						role = 'Manager'
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])

	driver.close()
		

	emailFile.close()
	instaFile.close()


def main(): # Main workflow of SoundCloud Scraper

	permalinks = []


	if os.path.exists("main_txt/rappers_unique.txt") or not os.path.exists("follower_boost_txt/following_permalink.txt"):
		print("main_txt/rappers_unique.txt detected. Perform following boost?")

		flag = ''
		while True:
			flag = input("Y or N: ")
			if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
				flag = flag.lower()
				break
			print("Please input Y or N.")
		if flag == 'y':
			unique_list = []
			with open('main_txt/rappers_unique.txt', 'r') as f:
				for item in f:
					unique_list.append(item.strip())
			for item in unique_list:
				generate_follower_permalinks(item)


	get_rapper_details()

main()
		