from selenium.webdriver.chrome.options import Options
import re

SCROLL_THRESHOLD = 500
DRIVER_PATH = 'chromedriver.exe'
DRIVER_OPTIONS = Options()
# DRIVER_OPTIONS.headless = True
DRIVER_OPTIONS.add_argument('--log-level=3')
DRIVER_OPTIONS.add_argument("--window-size=1920x1080")
INSTAGRAM_USERNAME_REGEX = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)
SCREENSHOT_UPLOAD_URL = 'https://example.com/images/'
SLUG_FILTER_PATTERN = re.compile('\W+')
PLAYLIST_SEARCH_PATH = 'https://soundcloud.com/search/sets?q=hip%20hop%20rap'
EMAIL_FILE_HEADER = ['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'HasInstagram', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'InLosAngeles']
INSTA_FILE_HEADER = ['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'InLosAngeles']


# Nikita Client ID
init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=212832-727922-185643-279192&client_id=FjnXkiGFvyaVIYtXadMm9pqIDawoxzUW&limit=200&offset={}&linked_partitioning=1&app_version=1627651107&app_locale=en"
profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=339301-954310-146236-973280&client_id=FjnXkiGFvyaVIYtXadMm9pqIDawoxzUW&limit=200&offset=0&linked_partitioning=1&app_version=1630392657&app_locale=en'

#Tom Client ID Sep 2021
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=2367%2C2371&facet=place&user_id=894984-656968-329615-449581&client_id=B31E7OJEB3BxbSbJBHarCQOhvKZUY09J&limit=200&offset={}&linked_partitioning=1&app_version=1631196797&app_locale=en"
# track_search_api = 'https://api-v2.soundcloud.com/search/tracks?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=2367%2C2371&facet=genre&user_id=894984-656968-329615-449581&client_id=B31E7OJEB3BxbSbJBHarCQOhvKZUY09J&limit=200&offset=0&linked_partitioning=1&app_version=1631196797&app_locale=en'
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=2367%2C2371&facet=place&user_id=894984-656968-329615-449581&client_id=B31E7OJEB3BxbSbJBHarCQOhvKZUY09J&limit=200&offset=0&linked_partitioning=1&app_version=1631196797&app_locale=en'

# AUDIOMACK

AUDIOMACK_INIT_URL = "https://audiomack.com/rap/trending-now"
EMAIL_FILE_HEADER_AUDIOMACK = ['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'HasInstagram', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'InLosAngeles']
INSTA_FILE_HEADER_AUDIOMACK = ['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'InstagramUserName', 'InstagramURL', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'InLosAngeles']
ALL_FILE_HEADER_AUDIOMACK = ['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'HasInstagram', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'InLosAngeles', 'HasEmail', 'HasSoundcloud', 'HasWebsite']
AUDIOMACK_API_BASE = 'https://api.audiomack.com/v1'
PHONE_NO_PATTERN = re.compile(r'^[a-zA-Z0-9]*((\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})[a-zA-Z]*$')
