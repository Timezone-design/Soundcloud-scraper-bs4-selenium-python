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
# import string


options = Options()
options.headless = True
options.add_argument('--log-level=3')
DRIVER_PATH = 'chromedriver.exe'
# printable = set(string.printable)

init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=930653-653278-774956-260140&client_id=J5Kk2YkB25TPuha9TgkuGg1VyIwz242r&limit=200&offset={}&linked_partitioning=1&app_version=1622628482&app_locale=en"

track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=genre&user_id=930653-653278-774956-260140&client_id=6JcMSl6wQUuPYeBzmXIOpxpp2VlPrIXE&limit=200&offset=0&linked_partitioning=1&app_version=1622710435&app_locale=en'

profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=930653-653278-774956-260140&client_id=6JcMSl6wQUuPYeBzmXIOpxpp2VlPrIXE&limit=200&offset=0&linked_partitioning=1&app_version=1622710435&app_locale=en'

# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset={}&linked_partitioning=1&app_version=1623250371&app_locale=en"

# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=genre&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=20&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'

# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=20&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'

instagram_username_regex = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

proxy_list = []

def remove_emoji(text):
	return emoji.get_emoji_regexp().sub(u'', text)


def clean_songtitle(songtitle):



def clean_artistname(artistname):
	artistname = artistname.replace('$', 's')
	artistname = artistname.replace('official', '')
	artistname = artistname.replace('Official', '')
	artistname = artistname.replace('"', '')
	artistname = artistname.replace("'", '')
	artistname = artistname.replace('_', ' ')
	artistname = artistname.replace('!', '')
	artistname = artistname.replace('?', '')

	artistname = artistname.title()
	words = artistname.split()
	for word in words:
		one_word = ""
		for i, char in enumerate(word):
			if i != 0:
				one_word.append(char)
			elif i > 1 and char.isupper() and word[i-1].islower() and word[i+1].islower():




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


def get_proxies():
	url = "https://free-proxy-list.net/"
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
	driver.set_page_load_timeout(10000)
	driver.get(url)
	time.sleep(2)
	country_select = driver.find_element_by_xpath('//*[@id="proxylisttable"]/tfoot/tr/th[3]/select/option[text()="US"]')
	country_select.click()
	soup = BeautifulSoup(driver.page_source, "html.parser")
	proxies = []
	for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
		tds = row.find_all("td")
		try:
			ip = tds[0].text.strip()
			port = tds[1].text.strip()
			host = f"{ip}:{port}"
			proxies.append(host)
		except IndexError:
			continue
	return proxies


def get_session(proxies):
	session = requests.Session()
	proxy = random.choice(proxies)
	session.proxies = {"http": proxy, "https": proxy}
	return session, proxy

def get_new_driver_from_proxy_list(proxy_list):
	s, p = get_session(proxy_list)
	options.add_argument("proxy-server={}".format(p))
	for i in range(25):
		try:
			driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH, service_log_path="NULL")
		except Exception as e:
			print(e)
			pass
		if driver:
			print("Proxy server changed to ", p)
			return driver
		elif i == 24:
			print("Cannot create webdriver from proxies.")
			exit(0)


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
		artistname = artistname.split('prod')[index]
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
		songtitle = songtitle.split('Feat')[0]
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
		songtitle = songtitle.split(',')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FT')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('FEAT')[0]
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
		songtitle = songtitle.split(' prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' Prod')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('PROD')[0]
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


	# driver = None

	# if use_auto_proxy:
	# 	driver = get_new_driver_from_proxy_list(proxy_list)

	# if use_manual_proxy:
	# 	pass

	# if not use_manual_proxy and not use_auto_proxy:


	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	genre_includes = get_genre_includes()
	print("Following genre will be included.")
	print(genre_includes)
	for permalink in permalinks:
		
		# if use_auto_proxy or use_manual_proxy and permalinks.index(permalink) % 20 == 0:
		# 	driver = get_new_driver_from_proxy_list(proxy_list)

		rapper_urls = []
		driver.set_page_load_timeout(10000)
		driver.get(permalink)
		time.sleep(2)
		scroll_pause_time = 1.5
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
				print("Scroll finished. Now scraping...")			
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

		with open('rappers.txt', 'a') as f:
			for item in rapper_urls:
				f.write("%s\n" % item)

		print("{} rapper profile URLs are written into file rappers.txt.".format(len(rapper_urls)))


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
		user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(permalink))).content.decode('utf-8'))
	except:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	
	if len(user_search['collection']) == 0:
		user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(username))).content.decode('utf-8'))
	if len(user_search['collection']) == 0:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	flag = False
	for item in user_search['collection']:
		if permalink in item['permalink']:
			user_object = item
			flag = True
			break
	if not flag:
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	location = user_object['city']
	country = user_object['country_code']
	permalink = user_object['permalink']
	fullname = user_object['full_name']
	username = user_object['username']

	# track_search = json.loads(requests.get(track_search_api.format(urllib.parse.quote(songtitlefull))).content.decode('utf-8'))
	# track_object = track_search['collection']

	# flag = False
	# for item in track_object:
	# 	if permalink in item['permalink_url']:
	# 		track_object = item
	# 		flag = True
	# 		break
	# if not flag:
	# 	return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	# try:
	# 	artistname = track_object['publisher_metadata']['artist']
	# except:
	# 	artistname = None
	# 	pass
	
	search_entity = []
	search_entity.append(username)
	search_entity.append(fullname)
	# search_entity.append(artistname)
	search_entity.append(songtitlefull)
	title_excludes = get_title_excludes()
	for entity in search_entity:
		for item in title_excludes:
			if entity is not None and item in entity:
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

	# if not username:
	# 	username = track_object['user']['username']
	# 	fullname = track_object['user']['full_name']

	if not fullname:
		fullname = username

	# if not artistname:
	artistname = username

	# if not location or not country:
	# 	try:
	# 		location = track_object['user']['city']
	# 		country = track_object['user']['country_code']
	# 	except:
	# 		location = ''
	# 		country = ''
	# 		pass

	songtitle = songtitlefull

	# get correct fullname and trackname

	# cleaning username
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
				return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"

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

		# artistname = replace_all(artistname)
		# try:
		# 	artistname = artistname.split('(')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split('[')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split('/')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split('|')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split(',')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split('&')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split(' x ')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split(' - ')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split(' ft')[0]
		# except:
		# 	pass
		# try:
		# 	artistname = artistname.split(' feat')[0]
		# except:
		# 	pass

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
		songtitle = songtitle.split('feat')[0]
	except:
		pass
	try:
		songtitle = songtitle.split(' x ')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('ft')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('Ft')[0]
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
		songtitle = songtitle.split('PROD.')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('produced by')[0]
	except:
		pass
	try:
		songtitle = songtitle.split('prod.')[0]
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
		return "excluded", "excluded", "excluded", "excluded", "excluded", "excluded", "excluded"
	if artistname:
		artistname = artistname.encode("ascii", "ignore")
		artistname = artistname.decode()

	artistname = clean_artistname(artistname)
	songtitle = clean_songtitle(songtitle)

	return username, fullname, artistname, location, country, songtitle, songtitlefull


def get_rapper_details():

	# initalizing csv files
	# write to new file everytime

	# filenameEmail = "Email-{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))
	# filenameInstagram = "Instagram-{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))

	filenameEmail = "Rappers with Email.csv"
	filenameInstagram = "Rappers with Instagram.csv"

	emailFile = open(filenameEmail, 'a', newline='', encoding='utf-8')
	instaFile = open(filenameInstagram, 'a', newline='', encoding='utf-8')

	emailwriter = csv.writer(emailFile, delimiter='\t')
	instawriter = csv.writer(instaFile, delimiter='\t')

	if os.path.getsize(filenameEmail) == 0:
		print("Writing a new file for Email")
		emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'Location', 'Country', 'Email', 'SongTitle', 'SongTitleFull'])
	if os.path.getsize(filenameInstagram) == 0:
		print("Writing a new file for Instagram")
		instawriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull'])

	rapper_profile_url = []
	rapper_profile_url_unique = []
	test_rapper_emails = []
	test_rapper_instagrams = []

	if not os.path.exists("rappers_unique.txt"): # check if unique series of data exists

		if os.path.exists("rappers.txt"): # if not, to see if it can be created from duplicate series
			with open('rappers.txt') as f:
				for item in f:
					rapper_profile_url.append(item)

			rapper_profile_url_unique = pd.unique(rapper_profile_url).tolist()
			rapper_profile_url_unique = [i.strip() for i in rapper_profile_url_unique]

			with open('permalinks.txt') as f:
				for item in f:
					if item.strip() in rapper_profile_url_unique:
						rapper_profile_url_unique.remove(item.strip())
						print(item.strip, "\tremoved for it appeared in permalinks.txt")

			url_deletion_list = ['beat', 'repost', 'network', 'prod']
			with open('rappers_unique.txt', 'w') as f:
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
			print("Please make rappers.txt first!")

	else:
		with open('rappers_unique.txt') as f:
			for item in f:
				rapper_profile_url_unique.append(item)

	print("{} unique rapper URLs detected.".format(len(rapper_profile_url_unique)))

	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
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
			username, fullname, artistname, location, country, songtitle, songtitlefull = get_other_info_of_rapper(rapper_soup, rapper.strip().split('/')[-1])
			if username == fullname == artistname == location == country == songtitle == songtitlefull == 'excluded':
				continue

			if rapper_email:
				emailwriter.writerow([rapper.strip(), username, fullname, artistname, location, country, rapper_email, songtitle, songtitlefull])
				print('Email written as: ', [rapper.strip(), username, fullname, artistname, location, country, rapper_email, songtitle, songtitlefull])
			
			if rapper_instagram_username:
				instawriter.writerow([rapper.strip(), username, fullname, artistname, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull])
				print('Insta written as: ', [rapper.strip(), username, fullname, artistname, location, country, rapper_instagram_username, rapper_instagram_url, songtitle, songtitlefull])
		

	emailFile.close()
	instaFile.close()


def main(): # Main workflow of SoundCloud Scraper

	permalinks = []

	"""

	use_auto_proxy = False
	use_manual_proxy = False

	while True:
		use_auto_proxy_string = input("Do you want to automatically select proxy? (y/n)")
		if use_auto_proxy_string.lower() != 'y' and use_auto_proxy_string.lower() != 'n':
			print("Please input Y or N for an answer")
			continue
		if use_auto_proxy_string.lower() == 'y':
			use_auto_proxy = True
		break

	if use_auto_proxy == False:
		while True:
			use_manual_proxy_string = input("Do you want to use manually chosen proxy? (y/n)")
			if use_manual_proxy_string.lower() != 'y' and use_manual_proxy_string.lower() != 'n':
				print("Please input	Y or N for an answer")
				continue
			if use_manual_proxy_string.lower() == 'y':
				use_manual_proxy = True
			break

	if use_auto_proxy:
		print('Searching for proxies...')
		proxy_list = get_proxies()
		print("Proxies found: \n", proxy_list)

	if use_manual_proxy == 'n':
		proxy_list = get_manual_proxies()
		print("Reading files for proxies")

	"""
		

	if not os.path.exists("permalinks.txt"): # Searches if permalinks to repost profiles are already made

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

			url = init_url.format(x * 200)

			api_response_object = json.loads(requests.get(url).content.decode('utf-8'))

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

		with open('permalinks.txt', 'w') as f: # Write permalinks of repost profiles to file

			for item in permalinks:

				f.write("%s\n" % item)

	else: # If permalinks are already existing in file

		with open('permalinks.txt') as f:

			for item in f:

				permalinks.append(item)

	print("\n\nOpening repost profiles to get rappers...")

	if not os.path.exists("rappers.txt"): # If rappers' profile urls are not scraped from repost profiles

		get_rapper_profile_urls_from_reposts(permalinks)

	get_rapper_details()

	




main()
		