import time
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
from datetime import datetime
import json
import requests
from constants import *
from resources import check_bio, get_bio_excludes, get_manager_bio_detect, generate_password, get_manager_email_detect, get_popularity, months, get_email_and_instagram_info_of_rapper, get_other_info_of_rapper, get_repost_excludes, get_endless_scroll_content, get_LA_includes



def generate_2nd_permalinks(driver):
	url = driver.current_url.rsplit('/', 1)[0] + '/likes'
	with open('additional_main_txt/position_of_rappers_unique_for_additional_permalink_from_main.txt', 'a') as f:
		f.write("%s\n" % datetime.now())
		f.write("%s\n\n" % url)
	print('Position saved to additional_main_txt/position_of_rappers_unique_for_additional_permalink_from_main.txt. Now scrolling page...')
	soup = get_endless_scroll_content(url)
	additional_rappers = []
	for rapper_profile in soup.find_all(class_="sound__header"):
		rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
		additional_rappers.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
		print(rapper_profile_url.attrs['href'], "\tis added to additional_main_txt/additional permalink.txt")

	with open('additional_main_txt/additional_permalink.txt', 'a') as additional_file:
		for item in additional_rappers:
			additional_file.write("%s\n" % item)
	print("\n{} additional repost urls are added.\n".format(len(additional_rappers)))
	driver.delete_all_cookies()


def get_rapper_profile_urls_from_reposts(permalinks):

	for permalink in permalinks:
		soup = get_endless_scroll_content(permalink + '/tracks')
		rapper_urls = []
		for rapper_profile in soup.find_all(class_="sound__header"):
			rapper_profile_url = rapper_profile.find(class_='soundTitle__username')
			rapper_urls.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))
			print(rapper_profile_url.attrs['href'], "\tis added")

		print("\n{} / {} repost urls are searched.\n".format(permalinks.index(permalink) + 1, len(permalinks)))

		with open('main_txt/rappers.txt', 'a') as f:
			for item in rapper_urls:
				f.write("%s\n" % item)

		print("{} rapper profile URLs are written into file main_txt/rappers.txt.".format(len(rapper_urls)))



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

	if not os.path.exists("main_txt/rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("main_txt/rappers.txt"): # if not, to see if it can be created from duplicate series
			with open('main_txt/rappers.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			with open('main_txt/permalinks.txt') as f:
				for item in f:
					if item.strip() in rapper_profile_url_unique:
						rapper_profile_url_unique.remove(item.strip())
						print(item.strip, "\tremoved for it appeared in permalinks.txt")

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('main_txt/rappers_unique.txt', 'w') as f:
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
			print("Please make main_txt/rappers.txt first!")

	else:
		with open('main_txt/rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item)

	print("{} unique rapper URLs detected.".format(len(rapper_profile_url_unique)))

	driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	driver.set_page_load_timeout(10000)

	print('This will create a list of unique rappers and also look in /likes to get a boost in resuts number.')
	print('Do you want to get only boost?')
	flag = ''
	while True:
		flag = input("Y or N: ")
		if isinstance(flag, str) and flag.lower() == 'y' or flag.lower() == 'n':
			flag = flag.lower()
			break
		print("Please input Y or N.")

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

		# check if there is error
		error_message = None
		try:
			error_message = rapper_soup.find('h1', class_='errorTitle')
			# write to no-user file
			if 'find' in error_message.get_text():
				with open('main_txt/rapper_with_deleted_profile', 'a') as f:
					f.write(rapper.strip())
					f.write('\n')
				print(f'{rapper.strip()} is enrolled to deleted profile txt.')
				continue
		except:
			pass

		bio = rapper_soup.find('div', class_='truncatedUserDescription__content')
		genre = ''
		role = 'Artist'


		if flag == 'y':
			generate_2nd_permalinks(driver)
			continue
		else:
			if not bio:
				print("Bio not detected. Passing to next url.")
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
		

	if not os.path.exists("main_txt/permalinks.txt"): # Searches if permalinks to repost profiles are already made

		print("Getting new permalinks...")

		while True: # Gets user input for API connection quantity
			
			api_conn_count = input("How many requests do you want to send? ")

			try:
				int(api_conn_count)
				break
			except Exception as e:
				print("Please input a valid integer.")
			else:
				pass
			finally:
				pass

		repost_excludes = get_repost_excludes()
		for x in range(int(api_conn_count)): # Send API request

			continue_flag = False
			url = init_url.format(x * 200)

			for iter in range(0, 100):
				try:
					api_response_object = json.loads(requests.get(url).content.decode('utf-8'))
				except:
					print("Error occured while fetching init url.")
					print("Consider updating your API.")
					sys.exit()
				
				try:
					temp = api_response_object["collection"]
					break
				except:
					if iter == 99:
						print("Error occured while fetching init url.")
						print("No object returned in search of 100 times. Nothing to worry, but if this persists, contact developer.")
						continue_flag = True
						break
					else:
						print("No object returned. Trying again for {}th lap.".format(iter + 2))
						continue
			
			if continue_flag:
				continue

			print("{}th api is sent.".format(x))

			if api_response_object["collection"] == []:

				print("No more profiles found. Total permalinks are {}.".format(len(permalinks)))

				break

			for single_response_object in api_response_object["collection"]:
				flag = False
				search_entity = single_response_object['permalink'] + ' ' + single_response_object['username'] + ' ' + single_response_object['full_name']
				for exclude_word in repost_excludes:
					if exclude_word in search_entity:
						flag = True
						break

				if flag:
					print("Excluded repost profile:", single_response_object["permalink_url"])
					continue

				permalinks.append(single_response_object["permalink_url"])

				print("{}th permalink added.".format(len(permalinks)))

		# permalinks_unique = pd.unique(permalinks).tolist() # Get non-duplicating profiles

		with open('main_txt/permalinks.txt', 'w') as f: # Write permalinks of repost profiles to file

			for item in permalinks:

				f.write("%s\n" % item)

	else: # If permalinks are already existing in file

		with open('main_txt/permalinks.txt') as f:

			for item in f:

				permalinks.append(item)

	print("\n\nOpening repost profiles to get rappers...")

	if not os.path.exists("main_txt/rappers.txt"): # If rappers' profile urls are not scraped from repost profiles

		get_rapper_profile_urls_from_reposts(permalinks)

	get_rapper_details()


main()
		