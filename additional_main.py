import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import sys
from datetime import datetime
from constants import *
from resources import check_bio, check_genre, get_bio_excludes, get_manager_bio_detect, generate_password, get_manager_email_detect, get_popularity, months, get_email_and_instagram_info_of_rapper, get_other_info_of_rapper, get_endless_scroll_content, get_LA_includes


RESCRAPE = False

if 0 <= 1 < len(sys.argv):
	if sys.argv[1] and sys.argv[1]=='--re-scrape':
		RESCRAPE = True
print("Rescrape key: ", RESCRAPE)
def generate_2nd_permalinks(url):
	url = url + '/likes'
	with open('additional_main_txt/position_of_rappers_unique_for_additional_permalink.txt', 'a') as f:
		f.write("%s\n" % datetime.now())
		f.write("%s\n\n" % url)
	print('Position saved to additional_main_txt/position_of_rappers_unique_for_additional_permalink.txt. Now scrolling page...')
	additional_rappers = []
	soup = get_endless_scroll_content(url)
	for rapper_profile in soup.find_all(class_="sound__header"):
		if check_genre(rapper_profile, 2, RESCRAPE):
			rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
			additional_rappers.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
			print(rapper_profile_url.attrs['href'], "\tis added to additional_main_txt/additional permalink.txt")

	with open('additional_main_txt/additional_permalink.txt', 'a') as additional_file:
		for item in additional_rappers:
			additional_file.write("%s\n" % item)
	print("\n{} additional repost urls are added.\n".format(len(additional_rappers)))


def get_rapper_profile_urls_from_reposts(permalinks):

	permalinks = pd.unique(permalinks).tolist()
	permalinks = [i.strip() for i in permalinks]

	for permalink in permalinks:
		try:
			rapper_urls = []
			soup = get_endless_scroll_content(permalink + '/likes')
			for rapper_profile in soup.find_all(class_="sound__header"):
				if check_genre(rapper_profile, 2, RESCRAPE):
					rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
					rapper_urls.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
					print(rapper_profile_url.attrs['href'], "\tis added")

			print("\n{} / {} repost urls are searched.\n".format(permalinks.index(permalink) + 1, len(permalinks)))

			with open('additional_main_txt/additional_rappers.txt', 'a') as f:
				for item in rapper_urls:
					f.write("%s\n" % item)

			print("{} rapper profile URLs are written into file additional_main_txt/additional_rappers.txt.".format(len(rapper_urls)))
		except: 
			print('Getting permalinks from /likes failed. Returning...')
			return

	
def get_rapper_details():

	filenameEmail = "csv/Rappers with Email updated.csv"
	filenameInstagram = "csv/Rappers with Instagram updated.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(EMAIL_FILE_HEADER)
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(INSTA_FILE_HEADER)

	rapper_profile_url = []
	rapper_profile_url_unique = []

	if not os.path.exists("additional_main_txt/additional_rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("additional_main_txt/additional_rappers.txt"): # if not, to see if it can be created from duplicate series
			with open('additional_main_txt/additional_rappers.txt') as f:
				for item in f:
					rapper_profile_url.append(item)
			with open('additional_main_txt/additional_permalink.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('additional_main_txt/additional_rappers_unique.txt', 'w') as f:
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
			print("Please make additional_main_txt/additional_rappers.txt first!")
			sys.exit()

	else:
		with open('additional_main_txt/additional_rappers_unique.txt') as f:
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

		if not check_genre(rapper_soup, 2, RESCRAPE):
			continue

		bio = rapper_soup.find('div', class_='truncatedUserDescription__content')
		genre = ''
		role = 'Artist'


		if not bio:
			print(rapper.strip() + "/tracks is excluded for there are no bio data.")
			continue
		if rapper_soup.find(class_='sc-tagContent'):
			genre = rapper_soup.find(class_='sc-tagContent').get_text()

		if not check_bio(bio):
			continue
		
		bio_text = bio.text
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


def main(): # Main workflow of SoundCloud Scraper

	permalinks = []

	if not os.path.exists("additional_main_txt/additional_permalink.txt"): # Searches if permalinks to repost profiles are already made
		print("additional_main_txt/additional_permalink not exist!")
		unique_list = []
		with open('main_txt/rappers_unique.txt', 'r') as f:
			for item in f:
				unique_list.append(item.strip())
		for item in unique_list:
			generate_2nd_permalinks(item)
	else: # If permalinks are already existing in file
		with open('additional_main_txt/additional_permalink.txt') as f:
			for item in f:
				permalinks.append(item)

	if os.path.exists("main_txt/rappers_unique.txt"):
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
			with open('main_txt/rappers_unique.txt', 'r') as f:
				for item in f:
					unique_list.append(item.strip())
			for item in unique_list:
				generate_2nd_permalinks(item)

	if not os.path.exists("additional_main_txt/additional_rappers.txt"): # If rappers' profile urls are not scraped from repost profiles
		get_rapper_profile_urls_from_reposts(permalinks)

	print("\n\nOpening additional repost profiles to get rappers...")

	get_rapper_details()


main()
		