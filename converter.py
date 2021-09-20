import csv
from numpy import e
import pandas as pd
from os import path
from resources import take_screenshot
from bs4 import BeautifulSoup


filenameEmail = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Rappers with Email updated.csv')
filenameCoupon = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Coupon Codes.csv')

if path.exists(filenameCoupon) == 0:
  print('Writing a new file for Coupon Code.')
  couponFile = open(filenameCoupon, 'w', newline='', encoding='utf-16')
  couponwriter = csv.writer(couponFile, delimiter='\t')
  couponwriter.writerow(['CouponCodeName', 'CouponCode', 'DiscountAmount', 'DiscountType', 'Uses', 'MaxUses', 'SingeUse', 'StartDate', 'Expiration', 'DiscountStatus', 'ProductCondition', 'ProductRequirements', 'IsItOnlyForSelectProducts', 'MinimumPurchasePrice'])
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

newlines = emaildf[~emaildf['CouponCode'].isin(coupondf['CouponCode'])].dropna(how = 'all')
newurls = newlines[['SoundCloudURL', 'ArtistNameCleaned', 'SongTitle']].copy()
newlines = newlines[['CouponCodeName', 'CouponCode']].copy()
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

print('Merge finished.')

if len(newlines.index) > 0:
  print('Now taking screenshots...')
  for index, url in enumerate(newurls['SoundCloudURL']):
    take_screenshot(url, newurls.iloc[index]['ArtistNameCleaned'], newurls.iloc[index]['SongTitle'])