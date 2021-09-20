import emoji
import string
import json
import os
import random
import datetime


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