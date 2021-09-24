import csv
import pandas as pd
from os import path
from resources import take_screenshot
from constants import SCREENSHOT_UPLOAD_URL


filenameEmail = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Rappers with Email updated.csv')
filenameCoupon = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Coupon Codes.csv')
filenameFinal = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Rappers with Email final.csv')

if not path.exists(filenameCoupon):
  print('Writing a new file for Coupon Code.')
  couponFile = open(filenameCoupon, 'w', newline='', encoding='utf-16')
  couponwriter = csv.writer(couponFile, delimiter='\t')
  couponwriter.writerow(['CouponCodeName', 'CouponCode', 'DiscountAmount', 'DiscountType', 'Uses', 'MaxUses', 'SingeUse', 'StartDate', 'Expiration', 'DiscountStatus', 'ProductCondition', 'ProductRequirements', 'IsItOnlyForSelectProducts', 'MinimumPurchasePrice'])
  couponFile.close()

if not path.exists(filenameFinal):
  print('Writing a new file for final csv.')
  couponFile = open(filenameCoupon, 'w', newline='', encoding='utf-16')
  couponwriter = csv.writer(couponFile, delimiter='\t')
  couponwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'ScreenshotFileName', 'ScreenshotURL'])
  couponFile.close()

emaildf = pd.read_csv(filenameEmail, encoding='utf-16', header=0, error_bad_lines=False, sep='\t')
coupondf = pd.read_csv(filenameCoupon, encoding='utf-16', header=0, error_bad_lines=False, sep='\t')

# print(list(emaildf.columns))

startdate = input('Start Date: ')
expiredate = input('Expiry Date: ')
dollaramount = input('Dollar Amount: ')

# print(emaildf['CouponCodeName'])

emaildf.drop_duplicates('CouponCodeName', inplace=True)
emaildf.reset_index(inplace=True)
emailextract = emaildf[['CouponCodeName', 'CouponCode']].copy()
couponextract = coupondf[['CouponCodeName', 'CouponCode']].copy()
print('Data extracted from Email csv')

newlines_all = emaildf[~emaildf['CouponCode'].isin(coupondf['CouponCode'])].dropna(how = 'all')
newlines = newlines_all[['ArtistNameCleaned', 'CouponCode']].copy()
newlines['ArtistNameCleaned'] = newlines['ArtistNameCleaned'].apply(lambda x: f'Discount -${dollaramount} for mp3 lease for {x}')
newlines.rename(columns={'ArtistNameCleaned': 'CouponCodeName'}, inplace=True)
newlines['DiscountAmount'] = dollaramount
newlines['DiscountType'] = 'flat'
newlines['Uses'] = '0/1'
newlines['MaxUses'] = 1
newlines['SingeUse'] = 1
newlines['StartDate'] = startdate
newlines['Expiration'] = expiredate
newlines['DiscountStatus'] = 'active'
newlines['ProductCondition'] = 'all'
newlines['ProductRequirements'] = ''
newlines['IsItOnlyForSelectProducts'] = '0'
newlines['MinimumPurchasePrice'] = ''
print('{} new entries found.'.format(len(newlines.index)))
if len(newlines.index) > 0:
  print('The first entry is {}.'.format(newlines.iloc[0]['CouponCodeName']))
  print('The last entry is {}.'.format(newlines.iloc[-1]['CouponCodeName']))
print('New lines are ready to be appended. Now merging...')
newlines.to_csv(filenameCoupon, mode='a', header=False, encoding='utf-16', sep='\t', index=False)
print('Merge finished and Coupon Codes.csv updated.')

if len(newlines.index) > 0:
  print('\nNow taking screenshots...')
  newlines_all['ScreenshotFileName'] = ''
  newlines_all['ScreenshotURL'] = ''

  for index, url in enumerate(newlines_all['SongLink']):
    filename = take_screenshot(url, newlines_all.iloc[index]['SoundCloudURL'].rsplit('/')[-1], newlines_all.iloc[index]['SongTitle'].rsplit()[0], newlines_all.iloc[index]['GO+'])
    if filename != 'None':
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotFileName')] = filename
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotURL')] = SCREENSHOT_UPLOAD_URL + filename
    else:
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotFileName')] = 'N/A'
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotURL')] = 'N/A'

  print('Moving to final csv')
  newlines_all.to_csv(filenameFinal, mode='a', header=False, encoding='utf-16', sep='\t', index=False)
