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


options = Options()
options.headless = True
options.add_argument('--log-level=3')
DRIVER_PATH = 'chromedriver.exe'
# printable = set(string.printable)

#VPS14 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=374055-868319-148378-438909&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=823653-254858-356082-610033&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=374055-868319-148378-438909&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS13 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=506656-214921-947718-308845&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=864563-351822-208584-426191&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=506656-214921-947718-308845&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS12 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=225221-581906-333282-235913&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=175086-459286-306569-656479&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=225221-581906-333282-235913&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS11 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=701279-440666-80283-875802&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=5790-421363-351543-605407&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=701279-440666-80283-875802&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS10 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=497234-797892-535463-757291&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=469817-885534-841096-316227&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=497234-797892-535463-757291&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS9 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=977037-489345-139741-290793&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=597296-764152-749432-143278&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=977037-489345-139741-290793&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS8 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=10600-120781-951139-20546&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset={}&linked_partitioning=1&app_version=1624617819&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=121245-10572-390322-318950&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=10600-120781-951139-20546&client_id=gYkVE2E1CDaIAQpIpP1FfmFt427RgSsv&limit=200&offset=0&linked_partitioning=1&app_version=1624617819&app_locale=en'

#VPS7 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS6 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS5 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS4 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS3 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS2 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS1 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&variant_ids=&facet=genre&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#Nikita Client ID
init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=212832-727922-185643-279192&client_id=bhdPp0QME8kXmKrbDc4gARDVv1v8JNQ3&limit=200&offset={}&linked_partitioning=1&app_version=1627651107&app_locale=en"
track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=genre&user_id=212832-727922-185643-279192&client_id=bhdPp0QME8kXmKrbDc4gARDVv1v8JNQ3&limit=200&offset=0&linked_partitioning=1&app_version=1627651107&app_locale=en'
profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=212832-727922-185643-279192&client_id=bhdPp0QME8kXmKrbDc4gARDVv1v8JNQ3&limit=200&offset=0&linked_partitioning=1&app_version=1627651107&app_locale=en'

#Tom Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset={}&linked_partitioning=1&app_version=1623250371&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=genre&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'

instagram_username_regex = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

proxy_list = []

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
		print(ex)
	return includes


def replace_all(text):
	text = re.sub(r'\bOfficial\b', "", text)
	text = re.sub(r'\bThe\b', "", text)
	text = re.sub(r'\bthe\b', "", text)
	text = re.sub(r'\bRapper\b', "", text)
	text = re.sub(r'\brapper\b', "", text)
	text = re.sub(r'\bda\b', "", text)
	text = re.sub(r'\btha\b', "", text)
	text = re.sub(r'\bmusic\b', "", text)
	text = re.sub(r'\bFeat\b', "", text)

	return text


def generate_2nd_permalinks(driver):
	url = driver.current_url + '/likes'
	driver.set_page_load_timeout(10000)
	driver.get(url)
	time.sleep(1)
	scroll_threshold = 10
	scroll_pause_time = 2
	genre_includes = get_genre_includes()
	print("Following genre will be included.")
	print(genre_includes)

	additional_rappers = []
	i = 0
	print('Now scrolling page...')
	while True:
		i += 1
		try:
			last_height = driver.execute_script("return document.body.scrollHeight")
			driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			time.sleep(scroll_pause_time)
			new_height = driver.execute_script("return document.body.scrollHeight")
			print('{}th scroll made.'.format(i))
		except:
			print("error in getting data. Passing to next iteration 21")
			return

		if last_height == new_height or i == scroll_threshold:
			print("Scroll finished. Now scraping... 21")			
			break

	soup = BeautifulSoup(driver.page_source, "html.parser")
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
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	genre_includes = get_genre_includes()
	print("Following genre will be included.")
	print(genre_includes)
	for permalink in permalinks:
		try:
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

			print("\n{} / {} repost urls are searched.\n".format(permalinks.index(permalink) + 1, len(permalinks)))

			with open('additional_rappers.txt', 'a') as f:
				for item in rapper_urls:
					f.write("%s\n" % item)

			print("{} rapper profile URLs are written into file additional_rappers.txt.".format(len(rapper_urls)))
		except:
			driver.close()
			return

	driver.close()


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
	print('1')
	try:
		songtitlefull = rapper_soup.find(class_='soundTitle__title').get_text().strip()
		username = rapper_soup.find(class_='profileHeaderInfo__userName').get_text().strip()
		user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(permalink))).content.decode('utf-8'))
	except:
		print('2')
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	
	if len(user_search['collection']) == 0:
		print('2')

		try:
			user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(username))).content.decode('utf-8'))
		except:
			return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	if len(user_search['collection']) == 0:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	print('1')

	flag = False
	for item in user_search['collection']:
		if permalink in item['permalink']:
			user_object = item
			flag = True
			break
	if not flag:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	print('1')

	location = user_object['city']
	country = user_object['country_code']
	permalink = user_object['permalink']
	fullname = user_object['full_name']
	username = user_object['username']

	songtitlefull = unicodedata.normalize('NFKC', songtitlefull)
	print('1')
	
	search_entity = []
	search_entity.append(username)
	search_entity.append(fullname)
	# search_entity.append(artistname)
	search_entity.append(songtitlefull)
	title_excludes = get_title_excludes()
	for entity in search_entity:
		for item in title_excludes:
			if entity is not None and item in entity:
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

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
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

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

	# if artistname == '':
	# 	artistname = fullname.strip()
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
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	if artistname:
		artistname = artistname.encode("ascii", "ignore")
		artistname = artistname.decode()

	artistnamecleaned = clean_artistname(artistname)
	print('cleaned artistname ', artistname)
	songtitle = clean_songtitle(songtitle)
	print('cleaned songtitle ', songtitle)

	return username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull


def get_rapper_details():

	filenameEmail = "Rappers with Email.csv"
	filenameInstagram = "Rappers with Instagram.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-16')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-16')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'SongTitle', 'SongTitleFull'])
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull'])

	rapper_profile_url = []
	rapper_profile_url_unique = []
	test_rapper_emails = []
	test_rapper_instagrams = []

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
		time.sleep(1)
		rapper_soup = BeautifulSoup(driver.page_source, "html.parser")
		bio = rapper_soup.find('div', class_='truncatedUserDescription__content')
		
		if not bio:
			continue

		bio_excludes = get_bio_excludes()
		bio_text = bio.text
		for item in bio_excludes:
			if item in bio_text:
				continue

		web_profiles = rapper_soup.find('div', class_="web-profiles")

		print('Searching {}th user as above url.'.format(rapper_profile_url_unique.index(rapper) + 1))

		rapper_email, rapper_instagram_username, rapper_instagram_url = get_email_and_instagram_info_of_rapper(bio, web_profiles)

		if rapper_email or rapper_instagram_username:
			username, fullname, artistname, artistnamecleaned, location, country, songtitle, songtitlefull = get_other_info_of_rapper(rapper_soup, rapper.strip().split('/')[-1])
			if username == fullname == artistname == artistnamecleaned == location == country == songtitle == songtitlefull == 'excluded':
				continue

			if rapper_email:
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, songtitle, songtitlefull])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_email, songtitle, songtitlefull])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, artistnamecleaned, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull])

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
		driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
		for item in unique_list:
			driver.get(item)
			generate_2nd_permalinks(driver)
		driver.close()
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
			driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
			for item in unique_list:
				driver.get(item)
				generate_2nd_permalinks(driver)
			driver.close()

	if not os.path.exists("additional_rappers.txt"): # If rappers' profile urls are not scraped from repost profiles
		get_rapper_profile_urls_from_reposts(permalinks)

	print("\n\nOpening additional repost profiles to get rappers...")

	get_rapper_details()

	




main()
		