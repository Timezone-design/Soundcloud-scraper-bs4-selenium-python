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


options = Options()
options.headless = True
DRIVER_PATH = 'chromedriver.exe'

init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=930653-653278-774956-260140&client_id=J5Kk2YkB25TPuha9TgkuGg1VyIwz242r&limit=200&offset={}&linked_partitioning=1&app_version=1622628482&app_locale=en"

track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=genre&user_id=930653-653278-774956-260140&client_id=6JcMSl6wQUuPYeBzmXIOpxpp2VlPrIXE&limit=20&offset=0&linked_partitioning=1&app_version=1622710435&app_locale=en'

profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=930653-653278-774956-260140&client_id=6JcMSl6wQUuPYeBzmXIOpxpp2VlPrIXE&limit=20&offset=0&linked_partitioning=1&app_version=1622710435&app_locale=en'

instagram_username_regex = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

proxy_list = []

def get_proxies():
    url = "https://free-proxy-list.net/"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
	driver.set_page_load_timeout(10000)
	driver.get(url)
	time.sleep(2)
	country_select = driver.find_element_by_xpath('//*[@id="proxylisttable"]/tfoot/tr/th[3]/select/option[text()="US"]')
	country_select.click()
    soup = bs(driver.page_source, "html.parser")
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


def song_title_and_rapper_name(name_title,index,index1):

	print('name_title: ', name_title)
	try:
		rapper_name = name_title.split('-')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('x ')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split(',')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('feat')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('Feat')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('prod')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('(')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('and')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('&')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('+')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('[')[index]
	except:
		pass
	try:
		rapper_name = rapper_name.split('|')[index]
	except:
		pass

	try:
		song_title = name_title.split('-')[index1] + name_title.split('-')[2]
	except:
		song_title = name_title.split('-')[index1]
	song_title_full = song_title

	try:
		song_title = song_title.split('(')[0]
	except:
		pass
	try:
		song_title = song_title.split('[')[0]
	except:
		pass
	try:
		song_title = song_title.split('feat')[0]
	except:
		pass
	try:
		song_title = song_title.split('Feat')[0]
	except:
		pass

	return rapper_name, song_title, song_title_full


def get_rapper_profile_urls_from_reposts(permalinks):

	if use_auto_proxy:

	if use_manual_proxy:


	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

	for permalink in permalinks:
		
		rapper_urls = []

		driver.set_page_load_timeout(10000)

		driver.get(permalink)

		time.sleep(2)

		scroll_pause_time = 1.5

		scroll_threshold = 10

		i = 0

		while True:
			
			i += 1

			last_height = driver.execute_script("return document.body.scrollHeight")

			driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

			time.sleep(scroll_pause_time)

			new_height = driver.execute_script("return document.body.scrollHeight")

			if last_height == new_height or i == scroll_threshold:

				print("Scroll finished. Now scraping...")
				
				break

		soup = BeautifulSoup(driver.page_source, "html.parser")

		for rapper_profile_url in soup.find_all(class_="soundTitle__username"):

			rapper_urls.append("https://soundcloud.com{}".format(rapper_profile_url.attrs['href']))

		print("{} / {} finished.".format(permalinks.index(permalink) + 1, len(permalinks)))

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
				instagram_username = instagram_username.attrs['href'].split(".com%2F")[1].split('&')[0] # split username from link
	
			except:
				instagram_username = None
				pass

		if instagram_username: # if found, remove ascii characters from the string

			if instagram_username[0] == "%":
				instagram_username = instagram_username[3:]

			try:
				instagram_username = instagram_username.split("%")[0]

			except:
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

	print("Email: ", email)

	print("Instagram: ", instagram_username)

	return email, instagram_username, instagram_url


def get_other_info_of_rapper(rapper_soup):

	songtitlefull = rapper_soup.find('a', class_='soundTitle__title').get_text().strip()

	track_search = json.loads(requests.get(track_search_api.format(urllib.parse.quote(songtitlefull))).content.decode('utf-8'))

	track_object = track_search['collection'][0]

	username = track_object['user']['username']
	fullname = track_object['user']['full_name']
	try:
		artistname = track_object['publisher_metadata']['artist']
	except:
		artistname = None
		pass
	location = track_object['user']['city']
	country = track_object['user']['country_code']

	if not username:
		username = rapper_soup.find('h3', class_='profileHeaderInfo__userName')
		username = username.h3.find(text=True, recursive=False)

	if not fullname:
		fullname = username

	if not artistname:
		artistname = username

	if not location or not country:
		user_search = json.loads(requests.get(profile_search_api.format(urllib.parse.quote(username))).content.decode('utf-8'))
		user_object = user_search['collection'][0]

		location = user_object['city']
		country = user_object['country_code']

	songtitle = songtitlefull

	if location == '':
		location = None

	if country == '':
		country = None

	# get correct fullname and trackname

	if '- ' in songtitlefull:
		temp_fullname, songtitle, songtitlefull = song_title_and_rapper_name(songtitlefull, 0, 1)
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
					temp_fullname, songtitle, songtitlefull = song_title_and_rapper_name(songtitlefull, 1, 0)
					break
				i += 1

	else:
		fullname = replace_all(username)
		try:
			fullname = fullname.split('(')[0]
		except:
			pass
		try:
			fullname = fullname.split('[')[0]
		except:
			pass
		try:
			fullname = fullname.split('|')[0]
		except:
			pass

		songtitle = songtitlefull
		try:
			songtitle = songtitlefull.split('(')[0]
		except:
			pass
		try:
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

	if artistname == '':
		artistname = fullname.strip()

	songtitle = songtitle.strip()
	if songtitle:
		songtitle = songtitle.encode("ascii", "ignore")
		songtitle = songtitle.decode()
	if artistname:
		artistname = artistname.encode("ascii", "ignore")
		artistname = artistname.decode()

	return username, fullname, artistname, location, country, songtitle, songtitlefull


def get_rapper_details():

	# initalizing csv files
	# write to new file everytime

	filenameEmail = "Email-{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))
	filenameInstagram = "Instagram-{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))

	emailFile = open(filenameEmail, 'w', newline='', encoding='utf-8')
	instaFile = open(filenameInstagram, 'w', newline='', encoding='utf-8')

	emailwriter = csv.writer(emailFile)
	instawriter = csv.writer(instaFile)

	emailwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'Location', 'Country', 'Email', 'SongTitle', 'SongTitleFull'])
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

			with open('rappers_unique.txt', 'w') as f:
				for item in rapper_profile_url_unique:
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
		web_profiles = rapper_soup.find('div', class_="web-profiles")

		print('Searching {}th user as above url.'.format(rapper_profile_url_unique.index(rapper) + 1))

		rapper_email, rapper_instagram_username, rapper_instagram_url = get_email_and_instagram_info_of_rapper(bio, web_profiles)

		if rapper_email or rapper_instagram_username:
			username, fullname, artistname, location, country, songtitle, songtitlefull = get_other_info_of_rapper(rapper_soup)
			
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

	use_auto_proxy = False
	use_manual_proxy = False

	while True:
		use_auto_proxy_string = input("Do you want to automatically select proxy? (y/n)")
		if use_auto_proxy_string.lowercase() != 'y' or use_auto_proxy_string.lowercase() != 'n':
			print("Please input Y or N for an answer")
			continue
		if use_auto_proxy_string.lowercase() == 'y':
			use_auto_proxy = True
		break

	if use_auto_proxy.lowercase() == 'n':
		while True:
			use_manual_proxy_string = input("Do you want to use manually chosen proxy? (y/n)")
			if use_manual_proxy_string.lowercase() != 'y' or use_manual_proxy_string.lowercase() != 'n':
				print("Please input	Y or N for an answer")
				continue
			if use_manual_proxy_string.lowercase() == 'y':
				use_manual_proxy = True
			break

	if use_auto_proxy:
		print('Searching for proxies...')
		proxy_list = get_proxies()
		print("Proxies found: \n", proxy_list)

	if use_manual_proxy.lowercase() == 'n':
		proxy_list = get_manual_proxies()
		print("Reading files for proxies")
		

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

		for x in range(int(api_conn_count)): # Send API request

			url = init_url.format(x * 200)

			api_response_object = json.loads(requests.get(url).content.decode('utf-8'))

			print("{}th api is sent.".format(x))

			if api_response_object["collection"] == []:

				print("No more profiles found. Total permalinks are {}.".format(len(permalinks)))

				break

			for single_response_object in api_response_object["collection"]:
				
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

	print("Getting repost profiles...")

	if not os.path.exists("rappers.txt"): # If rappers' profile urls are not scraped from repost profiles

		get_rapper_profile_urls_from_reposts(permalinks)

	get_rapper_details()

	




main()
		