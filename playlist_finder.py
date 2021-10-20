import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import sys
from datetime import datetime
from constants import *
from resources import check_genre, get_bio_excludes, get_genre_includes, get_manager_bio_detect, generate_password, get_manager_email_detect, get_popularity, months, get_email_and_instagram_info_of_rapper, get_other_info_of_rapper, get_endless_scroll_content


def get_rapper_details():

	filenameEmail = "csv/Rappers with Email updated.csv"
	filenameInstagram = "csv/Rappers with Instagram updated.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'HasInstagram', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState'])
	
	
	rapper_profile_url_unique = []
	print('Now scraping profiles...')
	print('---------------------------------------------------------------')
	print('---------------------------------------------------------------')
	print('---------------------------------------------------------------')
	print('Reading playlist_finder_txt/playlist_rappers_unique.txt for scraping...')
	if os.path.exists('playlist_finder_txt/playlist_rappers_unique.txt'):
		with open('playlist_finder_txt/playlist_rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item.strip())
	else:
		print('playlist_finder_txt/playlist_rappers_unique.txt not exists...')
		sys.exit()

	if len(rapper_profile_url_unique) == 0:
		print('Unique rapper URL count is 0. Rebuilding playlist unique rapper txt...')
		print('Reading playlist_rappers.txt')
		playlist_rappers = []
		with open('playlist_finder_txt/playlist_rappers.txt') as f:
			for item in f:
				playlist_rappers.append(item.strip())

		if len(playlist_rappers) == 0:
			print('Nothing found in playlist_rappers.txt. Make file to continue...')
			sys.exit()
		enrich_playlist_rappers_unique(playlist_rappers)

		print('Re-reading playlist rappers unique txt...')
		with open('playlist_finder_txt/playlist_rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item.strip())
	
	if len(rapper_profile_url_unique) == 0:
		print('No url found in playlist_rappers_unique.txt')
		sys.exit()

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

		print('\n\nRapper url: ', rapper.strip() + "/tracks")

		driver.get(rapper.strip() + "/tracks")
		time.sleep(2)
		rapper_soup = BeautifulSoup(driver.page_source, "html.parser")

		if not check_genre(rapper_soup, 2):
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
					songlink = rapper.strip()
			except:
				print('Error parsing couponcodes and popularity information. Moving to next iteration.')
				continue
				pass
				
			if rapper_email:
				manager_email = get_manager_email_detect()
				for item in manager_email:
					if item in rapper_email:
						role = 'Manager'
				has_instagram = 'No'
				if rapper_instagram_username:
					has_instagram = 'Yes'
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, rapper_instagram_username, rapper_instagram_url, has_instagram, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull, gostatus, 'https://soundcloud.com' + songlink, genre, role, followers, popularity, couponcodename, couponcode, songplays, uploaddate, popularityadjusted, activestatus])

	driver.close()
		

	emailFile.close()
	instaFile.close()


def enrich_playlist_profiles():
	currently_available = []
	if os.path.exists("playlist_finder_txt/playlist_profiles.txt"):
		with open("playlist_finder_txt/playlist_profiles.txt", 'r') as f:
			for item in f:
				currently_available.append(item.strip())
	print("Searching for playlist profiles...")
	appeared_list = []
	soup = get_endless_scroll_content(PLAYLIST_SEARCH_PATH)
	genre_includes = get_genre_includes()
		
	for item in soup.find_all(class_='sound__body'):
		try:
			genre = item.find('a', class_='soundTitle__tag').find('span').get_text()
		except:
			continue
			pass
		
		appeared = 'https://soundcloud.com' + item.find('a', class_='soundTitle__username').attrs['href']
		print("\nCurrent URL: ", appeared)
		if not appeared in appeared_list and not appeared in currently_available:
			appeared_list.append(appeared)
		else:
			print('This playlist occured before. Ignoring...')
			continue
		if not genre.strip() in genre_includes:
			print("Profile genre not match. Passing to next url.")
		else:
			with open("playlist_finder_txt/playlist_profiles.txt", 'a') as f:
				f.write(appeared + '\n')


def enrich_playlist_permalinks(playlist_profiles):
	currently_available = []
	if os.path.exists("playlist_finder_txt/playlist_permalinks.txt"):
		with open("playlist_finder_txt/playlist_permalinks.txt", 'r') as f:
			for item in f:
				currently_available.append(item.strip())
	
	print("Getting permalinks from playlist profiles...")

	for profile in playlist_profiles:
		soup = get_endless_scroll_content(profile + '/sets')
		genre_includes = get_genre_includes()
		
		for item in soup.find_all(class_='sound__body'):
			try:
				genre = item.find('a', class_='soundTitle__tag').find('span').get_text()
			except:
				continue
				pass
			
			appeared = 'https://soundcloud.com' + item.find('a', class_='sound__coverArt').attrs['href']
			print("\nCurrent URL: ", appeared)
			if not genre.strip() in genre_includes:
				print("Profile genre not match. Passing to next url.")
			else:
				with open("playlist_finder_txt/playlist_permalinks.txt", 'a') as f:
					f.write(appeared + '\n')

def enrich_playlist_rappers(playlist_permalinks):
	currently_available = []
	if os.path.exists("playlist_finder_txt/playlist_rappers.txt"):
		with open("playlist_finder_txt/playlist_rappers.txt", 'r') as f:
			for item in f:
				currently_available.append(item.strip())
	
	print("Getting rappers from playlist permalinks...")

	for profile in playlist_permalinks:
		soup = get_endless_scroll_content(profile)
		
		for item in soup.find_all(class_='trackItem__content'):
			appeared = 'https://soundcloud.com' + item.find('a', class_='trackItem__username').attrs['href']
			print("\nCurrent URL: ", appeared)
			with open("playlist_finder_txt/playlist_rappers.txt", 'a') as f:
				f.write(appeared + '\n')


def enrich_playlist_rappers_unique(playlist_rappers):
	print("Making list of unique profiles...")

	look_in = []
	print('Reading original permalinks.txt...')
	if os.path.exists('main_txt/permalinks.txt'):
		with open('main_txt/permalinks.txt') as f:
			for item in f:
				if not item.strip() in look_in:
					look_in.append(item.strip())
	else:
		print('Original permalinks.txt not exists...')

	print('Reading main_txt/rappers_unique.txt')
	if os.path.exists('main_txt/rappers_unique.txt'):
		with open('main_txt/rappers_unique.txt') as f:
			for item in f:
				if not item.strip() in look_in:
					look_in.append(item.strip())
	else:
		print('main_txt/rappers_unique.txt not exists...')

	print('Reading additional_main_txt/additional_rappers_unique.txt')
	if os.path.exists('additional_main_txt/additional_rappers_unique.txt'):
		with open('additional_main_txt/additional_rappers_unique.txt') as f:
			for item in f:
				if not item.strip() in look_in:
					look_in.append(item.strip())
	else:
		print('additional_main_txt/additional_rappers_unique.txt not exists...')

	print('Reading follower_boost_txt/following_rappers_unique.txt')
	if os.path.exists('follower_boost_txt/following_rappers_unique.txt'):
		with open('follower_boost_txt/following_rappers_unique.txt') as f:
			for item in f:
				if not item.strip() in look_in:
					look_in.append(item.strip())
	else:
		print('follower_boost_txt/following_rappers_unique.txt not exists...')

	print('Reading playlist_finder_txt/playlist_rappers_unique.txt')
	if os.path.exists('playlist_finder_txt/playlist_rappers_unique.txt'):
		with open('playlist_finder_txt/playlist_rappers_unique.txt') as f:
			for item in f:
				if not item.strip() in look_in:
					look_in.append(item.strip())
	else:
		print('playlist_finder_txt/playlist_rappers_unique.txt not exists...')

	temp_list = []
	for item in playlist_rappers:
		if not item.strip() in look_in:
			temp_list.append(item.strip())

	print('Writing playlist_rappers_unique.txt')
	with open('playlist_finder_txt/playlist_rappers_unique.txt', 'w') as f:
		for item in temp_list:
			f.write(item + '\n')


def main(): # Main workflow of SoundCloud Scraper

	# ---------------------------------------------
	# Making/Enriching playlist_profiles.txt
	# ---------------------------------------------
	if os.path.exists("playlist_finder_txt/playlist_profiles.txt"):
		print("playlist_profiles.txt exists. Do you want to get more playlist profiles?")
	else:
		print("playlist_profiles.txt exists. Do you want to make playlist profiles?")
	flag = ''
	while True:
		flag = input("Y or N: ")
		if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
			flag = flag.lower()
			break
		print("Please input Y or N.")
	if flag == 'y':
		enrich_playlist_profiles()

	if not os.path.exists("playlist_finder_txt/playlist_profiles.txt"):
		enrich_playlist_profiles()

	print('Reading playlist_profiles.txt')
	playlist_profiles = []
	with open('playlist_finder_txt/playlist_profiles.txt') as f:
		for item in f:
			playlist_profiles.append(item.strip())
	
	if len(playlist_profiles) == 0:
		print('Nothing found in playlist_profiles.txt. Making file...')
		enrich_playlist_profiles()

	# ---------------------------------------------
	# Making/Enriching playlist_permalinks.txt
	# ---------------------------------------------

	if os.path.exists("playlist_finder_txt/playlist_permalinks.txt"):
		print("playlist_permalinks.txt exists. Do you want to get more permalinks?")
		flag = ''
		while True:
			flag = input("Y or N: ")
			if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
				flag = flag.lower()
				break
			print("Please input Y or N.")
		if flag == 'y':
			print('Enriching playlist_permalink.txt')
			enrich_playlist_permalinks(playlist_profiles)
	else:
		print('Making playlist_permalink.txt')
		enrich_playlist_permalinks(playlist_profiles)

	print('Reading playlist_permalink.txt')
	playlist_permalinks = []
	with open('playlist_finder_txt/playlist_permalinks.txt') as f:
		for item in f:
			playlist_permalinks.append(item.strip())
			
	if len(playlist_permalinks) == 0:
		print('Nothing found in playlist_permalinks.txt. Make file to continue...')
		sys.exit()

	# ---------------------------------------------
	# Making/Enriching playlist_rappers.txt
	# ---------------------------------------------

	if os.path.exists("playlist_finder_txt/playlist_rappers.txt"):
		print("playlist_rappers.txt exists. Do you want to get more rappers?")
		flag = ''
		while True:
			flag = input("Y or N: ")
			if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
				flag = flag.lower()
				break
			print("Please input Y or N.")
		if flag == 'y':
			print('Enriching playlist_rappers.txt')
			enrich_playlist_rappers(playlist_permalinks)
	else:
		print('Making playlist_rappers.txt')
		enrich_playlist_rappers(playlist_permalinks)

	print('Reading playlist_rappers.txt')
	playlist_rappers = []
	with open('playlist_finder_txt/playlist_rappers.txt') as f:
		for item in f:
			playlist_rappers.append(item.strip())

	if len(playlist_rappers) == 0:
		print('Nothing found in playlist_rappers.txt. Make file to continue...')
		sys.exit()

	# ---------------------------------------------
	# Making/Enriching playlist_rappers_unique.txt
	# ---------------------------------------------
	if os.path.exists("playlist_finder_txt/playlist_rappers_unique.txt"):
		enrich_playlist_rappers_unique(playlist_rappers)
	else:
		get_rapper_details()

main()
		