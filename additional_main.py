import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import urllib.parse
import csv
import pandas as pd
import emoji
import string
import unicodedata
import sys
from datetime import datetime, date
import random


options = Options()
options.headless = True
options.add_argument('--log-level=3')
DRIVER_PATH = 'chromedriver.exe'
# printable = set(string.printable)

#VPS14 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=374055-868319-148378-438909&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS13 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=506656-214921-947718-308845&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS12 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=225221-581906-333282-235913&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS11 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=701279-440666-80283-875802&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS10 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=497234-797892-535463-757291&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS9 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=977037-489345-139741-290793&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS8 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=10600-120781-951139-20546&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS7 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS6 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS5 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS4 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS3 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS2 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS1 Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#Nikita Client ID
profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=339301-954310-146236-973280&client_id=2FBT7dRlnJnnGKXjivkUCFLmzLG80Rur&limit=200&offset=0&linked_partitioning=1&app_version=1630392657&app_locale=en'

#Tom Client ID
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'

instagram_username_regex = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

def remove_emoji(text):
	return emoji.get_emoji_regexp().sub(u'', text)


def clean_songtitle(songtitle):
	songtitle = songtitle.strip()
	songtitle = string.capwords(songtitle)
	return songtitle

def clean_artistname(artistname):
	artistname = artistname.strip()
	artistname = artistname.replace('$', 's')
	artistname = artistname.replace('official', '')
	artistname = artistname.replace('Official', '')
	artistname = artistname.replace('OFFICIAL', '')
	artistname = artistname.replace('"', '')
	artistname = artistname.replace('_', ' ')
	artistname = artistname.replace('!', '')
	artistname = artistname.replace('?', '')
	artistname = artistname.replace('*', ' ')
	if len(artistname) > 2 and artistname[-2:] == '//':
		artistname = artistname[:-2]
	if len(artistname) > 1 and artistname[-1] == '.':
		artistname = artistname[:-1]
	if len(artistname) > 1 and artistname[-1] == '/':
		artistname = artistname[:-1]
	if len(artistname) > 1 and artistname[0] == "'":
		artistname = artistname[1:]
	if len(artistname) > 1 and artistname[-1] == "'":
		artistname = artistname[:-1]
	if artistname[:4].lower() == 'user' and artistname[5:].isnumeric():
		artistname = 'man'

	artistname = string.capwords(artistname)

	return artistname.strip()


def get_bio_excludes():
	excludes = []
	try:
		if os.path.exists('bio.exclude.json'):
			with open('bio.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for bio.exclude.json.")
		print(ex)
	return excludes


def get_title_excludes():
	excludes = []
	try:
		if os.path.exists('title.exclude.json'):
			with open('title.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				# print("title excludes returned: ", excludes)
				return excludes
	except Exception as ex:
		print("JSON reading failed for title.exclude.json.")
		print(ex)
	return excludes


def get_famous_rapper_excludes():
	excludes = []
	try:
		if os.path.exists('famous_rapper.exclude.json'):
			with open('famous_rapper.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for famous_rapper.exclude.json.")
		print(ex)
	return excludes


def get_email_excludes():
	excludes = []
	try:
		if os.path.exists('email.exclude.json'):
			with open('email.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for email.exclude.json.")
		print(ex)
	return excludes


def get_repost_excludes():
	excludes = []
	try:
		if os.path.exists('repost.exclude.json'):
			with open('repost.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for repost.exclude.json.")
		print(ex)
	return excludes


def get_genre_includes():
	includes = []
	try:
		if os.path.exists('genre.include.json'):
			with open('genre.include.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for genre.include.json.")
		print(ex)
	return includes


def get_manager_bio_detect():
	includes = []
	try:
		if os.path.exists('managerbiodetect.json'):
			with open('managerbiodetect.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for managerbiodetect.json.")
		print(ex)
	return includes


def get_manager_email_detect():
	includes = []
	try:
		if os.path.exists('managermaildetect.json'):
			with open('managermaildetect.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for managermaildetect.json.")
		print(ex)
	return includes


def generate_password(size=10):
	chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
	return ''.join(random.choice(chars) for _ in range(size))


def months(d1, d2):
	return d1.month - d2.month + 12*(d1.year - d2.year)


def get_popularity(soup, followers):
	for index, item in enumerate(soup.find_all(class_='sound__body')):
		goplus = item.find(class_='tierIndicator__smallGoPlus')
		if not 'sc-hidden' in goplus['class']:
			print('A track skipped as it is a GO+.')
			continue
		uploaddate = item.find(class_='soundTitle__uploadTime').find('time')['datetime'].split('T')[0]
		uploaddateobj = datetime.fromisoformat(uploaddate)
		uploadedmonth = months(datetime.today(), uploaddateobj)
		if uploadedmonth >= 2:
			print('{}th upload is selected for popularity verification.'.format(index + 1))
			try:
				songplay = int(item.find('li', class_='sc-ministats-item').find(class_='sc-visuallyhidden').text.split()[0].replace(',', ''))
			except:
				songplay = 0
				pass

			try:
				comments = int(item.find_all('li', class_='sc-ministats-item')[1]['title'].split()[0].replace(',', ''))
			except:
				comments = 0
				pass
			
			if songplay / followers < 0.04 and comments < 5:
				return 'fake'
			else:
				return 'True'

	
def generate_2nd_permalinks(url):
	url = url + '/likes'
	tempdriver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
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

	



def song_title_and_artist_name(songtitlefull,index,index1):

	print('songtitlefull: ', songtitlefull)
	artistname = songtitlefull
	try:
		artistname = artistname.split('-')[index]
	except:
		pass
	try:
		artistname = artistname.split('x ')[index]
	except:
		pass
	try:
		artistname = artistname.split('X ')[index]
	except:
		pass
	try:
		artistname = artistname.split(',')[index]
	except:
		pass
	try:
		artistname = artistname.split('feat')[index]
	except:
		pass
	try:
		artistname = artistname.split('Feat')[index]
	except:
		pass
	try:
		artistname = artistname.split('FEAT')[0]
	except:
		pass
	try:
		artistname = artistname.split('ft')[0]
	except:
		pass
	try:
		artistname = artistname.split('Ft')[0]
	except:
		pass
	try:
		artistname = artistname.split('FT')[0]
	except:
		pass
	try:
		artistname = artistname.split('featuring')[0]
	except:
		pass
	try:
		artistname = artistname.split('Featuring')[0]
	except:
		pass
	try:
		artistname = artistname.split('FEATURING')[0]
	except:
		pass
	try:
		artistname = artistname.split(' prod')[0]
	except:
		pass
	try:
		artistname = artistname.split(' Prod')[0]
	except:
		pass
	try:
		artistname = artistname.split(' PROD')[0]
	except:
		pass
	try:
		artistname = artistname.split('(')[index]
	except:
		pass
	try:
		artistname = artistname.split('and')[index]
	except:
		pass
	try:
		artistname = artistname.split('&')[index]
	except:
		pass
	try:
		artistname = artistname.split('+')[index]
	except:
		pass
	try:
		artistname = artistname.split('[')[index]
	except:
		pass
	try:
		artistname = artistname.split('|')[index]
	except:
		pass


	try:
		songtitle = songtitlefull.split('-')[index1] + songtitlefull.split('-')[2]
	except:
		songtitle = songtitlefull.split('-')[index1]
	try:
		songtitle = songtitle.split('(')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('[')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('feat')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('feat.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Feat')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Feat.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEAT')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEAT.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(':')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('@')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('#')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' x ')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' X ')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(',')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FT')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FT.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('featuring')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Featuring')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEATURING')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_PROD')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PROD')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' pro')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' Pro')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' By')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('+')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('*')[0]
	except:
		pass
	try:
		if songtitle[0] == '@':
			songtitle = ' '.join(songtitle.split()[1:])
	except:
		pass
	return artistname, songtitle


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
			driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
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

	


def get_email_and_instagram_info_of_rapper(bio, web_profiles):

	email = None

	instagram_username = None

	instagram_url = None

	if web_profiles != None:
		instagram_username = web_profiles.select_one("a[href*=instagram]") # select href with instagram in it

		if instagram_username:

			try:
				instagram_username = urllib.parse.unquote(instagram_username.attrs['href']).split(".com/")[1] # split username from link
				if instagram_username[:2] == 'p/':
					instagram_username = instagram_username[2:]
				if '/' in instagram_username:
					instagram_username = instagram_username.split('/')[0]
				if '#' in instagram_username:
					instagram_username = instagram_username.split('#')[0]
				if '?' in instagram_username:
					instagram_username = instagram_username.split('?')[0]
				if '&' in instagram_username:
					instagram_username = instagram_username.split('&')[0]
	
			except:
				instagram_username = None
				pass


	if bio != None:

		email = bio.select_one("a[href*=mailto]") # Searches href with mailto: in it

		if email:
			email = email.attrs['href'].split(":")[1] # get email address after mailto:
			bio = bio.text

		else:
			bio = bio.text
			email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', bio) # if email is not found as a link, searches email from texts

			if email:
				email = email.group(0)

		if instagram_username == None:
			searched = instagram_username_regex.search(bio) # if instagram_username is not found in web_profiles

			if searched:
				instagram_username = searched.group(2)

	if instagram_username:
		instagram_url = "https://www.instagram.com/" + instagram_username # generate url from username

	if email:
		email = email.encode("ascii", "ignore")
		email = email.decode()
		if not email.find(":") == -1:
			email = email.split(":")[1]
		if not email.find("/") == -1:
			email = email.split("//")[1]
		email_excludes = get_email_excludes()
		for item in email_excludes:
			if item in email:
				return None, None, None

	print("Email: ", email)

	print("Instagram: ", instagram_username)

	return email, instagram_username, instagram_url


def get_other_info_of_rapper(rapper_soup, permalink):
	try:
		songtitlefull = rapper_soup.find(class_='soundTitle__title').get_text().strip()
		username = rapper_soup.find(class_='profileHeaderInfo__userName').get_text().strip()
	except:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	try:
		user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(permalink))).content.decode('utf-8'))
	except:
		print("Error occured while using user search API in https://soundcloud.com/" + permalink + "\n")
		print("Consider updating your API.")
		sys.exit()

	if len(user_search['collection']) == 0:
		try:
			user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(username))).content.decode('utf-8'))
		except:
			print("Error occured while using user search API in https://soundcloud.com/" + permalink + "\n")
			print("Consider updating your API.")
			sys.exit()
			
	if len(user_search['collection']) == 0:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	flag = False
	for item in user_search['collection']:
		if permalink in item['permalink']:
			user_object = item
			flag = True
			break
	if not flag:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	followers = user_object['followers_count']
	popularity = 'unknown'
	if followers >= 10000:
		popularity = 'trending'
	if followers >= 50000:
		popularity = 'hot'
	if followers >= 100000:
		popularity = 'popular'
	if followers >= 250000:
		popularity = 'famous'
	if followers >= 500000:
		popularity = 'infamous'
	location = user_object['city']
	country = user_object['country_code']
	permalink = user_object['permalink']
	fullname = user_object['full_name']
	username = user_object['username']

	songtitlefull = unicodedata.normalize('NFKC', songtitlefull)
	
	search_entity = []
	search_entity.append(username)
	search_entity.append(fullname)
	# search_entity.append(artistname)
	search_entity.append(songtitlefull)
	title_excludes = get_title_excludes()
	for entity in search_entity:
		for item in title_excludes:
			if entity is not None and item in entity:
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	if not fullname:
		fullname = username

	artistname = username

	songtitle = songtitlefull

	username = remove_emoji(username)
	username = re.sub(r'[^\x00-\x7f]', r'', username)
	username = username.strip()
	try:
		if username[0] == '(' and ')' in username:
			username = username[1:].replace(')', '')
		if username[0] == '@':
			username = username[1:]
		if username[0] == '|':
			username = username[1:]
		if username[0] == '#':
			username = username[1:]
		if username[0] == '[' and ']' in username:
			username = username[1:].replace(']', '')
		if username[0] == '{' and '}' in username:
			username = username[1:].replace('}', '')
		if username[0] == '<' and '>' in username:
			username = username[1:].replace('>', '')
		if '@' in username:
			username = username.split('@')[0]
		if '#' in username:
			username = username.split('#')[0]
		if '(' in username:
			username = username.split('(')[0]
		if '[' in username:
			username = username.split('[')[0]
		if '{' in username:
			username = username.split('{')[0]
		if '|' in username:
			username = username.split('|')[0]
		username = username.strip()
	except:
		pass

	preceding_words = ["Prod. by", "Prod. By", "prod. by", "prod by", "Prod by", "Prod By", "PROD. BY", "PROD BY", "Produced by", "ProducedBy", "produced by", "beat by", "Beat By", "Beat by", "Beat By", "Prod", "prod"]
	if username in songtitlefull:
		for word in preceding_words:
			if word + username in songtitlefull or '-' + word in songtitlefull or '- ' + word in songtitlefull:
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	# if re.search(r'\(([^)]+)-([^)]+)\)', songtitlefull):
	# 	print(re.search(r'\(([^)]+)-([^)]+)\)', songtitlefull))

	if '- ' in songtitlefull:
		temp_fullname, songtitle = song_title_and_artist_name(songtitlefull, 0, 1)
		username_list = username.split()
		songtitle_list = songtitle.split()
		fullname2_list = artistname.split()

		counter = 0
		flag_user_name_match = False
		flag_full_name2_match = False
		for sn in songtitle_list:
			for us in username_list:
				if sn == us:
					counter += 1
				if counter == 2:
					flag_user_name_match = True
					break
			if flag_user_name_match:
				break

		lengthOfsongtitle = len(songtitle_list)
		i = 1
		if not flag_user_name_match:
			counter = 0
			for sn in songtitle_list:
				for fn in fullname2_list:
					if sn == fn:
						counter += 1
					if counter == 2:
						flag_full_name2_match = True
						break
				if flag_full_name2_match:
					temp_fullname, songtitle = song_title_and_artist_name(songtitlefull, 1, 0)
					break
				i += 1


	try:
		if not songtitle[0] == '(':
			songtitle = songtitle.split('(')[0]
		if not songtitle[0] == "[":
			songtitle = songtitle.split('[')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Feat')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Feat.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('feat')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('feat.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEAT')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEAT.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' x ')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' X ')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FT')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FT.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('/')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('|')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('+')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FREE] ')[1]
	except:
		pass
	try:
		songtitle = songtitle.split(':')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('?')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Mixed by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Mixed By')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('mixed by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-PROD')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('-PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('_PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('prod.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PROD')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('produced by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Produced by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Produced By')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PRODUCED')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('beat by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Beat by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Beat By')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('BEAT BY')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('¨')[0]
	except:
		pass
	try:
		if songtitle[0] == '#':
			songtitle = ' '.join(songtitle.split()[1:])
	except:
		pass
	try:
		songtitle = songtitle.replace('"', '')
		songtitle = songtitle.replace("'", "")
	except:
		pass
	src_str  = re.compile("freestyle", re.IGNORECASE)
	songtitle  = src_str.sub('', songtitle)

	artistname = username
	famous_rapper_excludes = get_famous_rapper_excludes()
	for item in famous_rapper_excludes:
		if item in artistname:
			artistname = 'man'
			break

	songtitle = songtitle.strip()
	if songtitle:
		songtitle = songtitle.encode("ascii", "ignore")
		songtitle = songtitle.decode()
	else:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	if artistname:
		artistname = artistname.encode("ascii", "ignore")
		artistname = artistname.decode()

	artistnamecleaned = clean_artistname(artistname)
	print('cleaned artistname ', artistname)
	songtitle = clean_songtitle(songtitle)
	print('cleaned songtitle ', songtitle)

	return username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull, followers, popularity


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

	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
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
		