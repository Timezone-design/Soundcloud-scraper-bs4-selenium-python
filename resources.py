import emoji
import string
import json
import os
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import re
import urllib.parse
import requests
import unicodedata
import sys
from constants import *
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
		if os.path.exists('json/bio.exclude.json'):
			with open('json/bio.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for json/bio.exclude.json.")
		print(ex)
	return excludes


def get_title_excludes():
	excludes = []
	try:
		if os.path.exists('json/title.exclude.json'):
			with open('json/title.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				# print("title excludes returned: ", excludes)
				return excludes
	except Exception as ex:
		print("JSON reading failed for json/title.exclude.json.")
		print(ex)
	return excludes


def get_famous_rapper_excludes():
	excludes = []
	try:
		if os.path.exists('json/famous_rapper.exclude.json'):
			with open('json/famous_rapper.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for json/famous_rapper.exclude.json.")
		print(ex)
	return excludes


def get_email_excludes():
	excludes = []
	try:
		if os.path.exists('json/email.exclude.json'):
			with open('json/email.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for json/email.exclude.json.")
		print(ex)
	return excludes


def get_repost_excludes():
	excludes = []
	try:
		if os.path.exists('json/repost.exclude.json'):
			with open('json/repost.exclude.json') as fd:
				obj = json.loads(fd.read())
				excludes = obj['excludes']
				return excludes
	except Exception as ex:
		print("JSON reading failed for json/repost.exclude.json.")
		print(ex)
	return excludes


def get_genre_includes():
	includes = []
	try:
		if os.path.exists('json/genre.include.json'):
			with open('json/genre.include.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for json/genre.include.json.")
		print(ex)
	return includes


def get_manager_bio_detect():
	includes = []
	try:
		if os.path.exists('json/managerbiodetect.json'):
			with open('json/managerbiodetect.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for json/managerbiodetect.json.")
		print(ex)
	return includes


def get_manager_email_detect():
	includes = []
	try:
		if os.path.exists('json/managermaildetect.json'):
			with open('json/managermaildetect.json') as fd:
				obj = json.loads(fd.read())
				includes = obj['includes']
				return includes
	except Exception as ex:
		print("JSON reading failed for json/managermaildetect.json.")
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
		if not goplus:
			continue
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
			searched = INSTAGRAM_USERNAME_REGEX.search(bio) # if instagram_username is not found in web_profiles

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
			searched = INSTAGRAM_USERNAME_REGEX.search(bio) # if instagram_username is not found in web_profiles

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


def take_screenshot(url, username, title):
	print("Opening driver for screenshot...")
	driver = webdriver.Chrome(options=DRIVER_OPTIONS, executable_path=DRIVER_PATH)
	try:
		driver.set_page_load_timeout(10000)
		driver.get(url + '/tracks')
		link = driver.find_element_by_class_name('soundTitle__title').get_attribute('href')
		driver.get(link)
		time.sleep(2)

		print('Driver opened. Now moving cursor...')
		target = driver.find_element_by_class_name('playbackTimeline__progressBar')
		bar = driver.find_element_by_class_name('listenContext')
		action = ActionChains(driver)
		# action.move_to_element_with_offset(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'playbackTimeline__progressBar'))), 100, 0).click().perform()
		action.move_to_element_with_offset(target, 100, 0).click().perform()
		action.move_to_element_with_offset(bar, 10, 10).perform()
		print('Cursor moved. Now taking screenshot...')
		driver.save_screenshot(os.path.join('screenshots', '{}.{}.png'.format(username, title)))
		driver.close()
		print('Screenshot saved in the name of {}.{}.png'.format(username, title))
		print('\n')
	except:
		print('screenshot failed to be created.')
		pass

	try:
		driver.close()
	except:
		pass