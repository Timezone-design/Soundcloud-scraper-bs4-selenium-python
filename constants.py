from selenium.webdriver.chrome.options import Options
import re

SCROLL_THRESHOLD = 500
DRIVER_PATH = 'chromedriver.exe'
DRIVER_OPTIONS = Options()
DRIVER_OPTIONS.headless = True
DRIVER_OPTIONS.add_argument('--log-level=3')
INSTAGRAM_USERNAME_REGEX = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

#VPS7 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=434708-293573-67871-677944&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS6 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=629348-114058-775559-561393&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS5 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=43605-488002-732889-712556&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS4 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=793243-845133-680818-351036&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS3 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=716706-30782-53008-419962&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS2 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=993249-877589-480335-264294&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#VPS1 Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&variant_ids=&facet=place&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset={}&linked_partitioning=1&app_version=1623409080&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=517948-175441-226179-487079&client_id=Gef7Kyef9qUHLjDFrmLfJTGqXRS9QT3l&limit=200&offset=0&linked_partitioning=1&app_version=1623409080&app_locale=en'

#Nikita Client ID
init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=212832-727922-185643-279192&client_id=bhdPp0QME8kXmKrbDc4gARDVv1v8JNQ3&limit=200&offset={}&linked_partitioning=1&app_version=1627651107&app_locale=en"
profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=339301-954310-146236-973280&client_id=2FBT7dRlnJnnGKXjivkUCFLmzLG80Rur&limit=200&offset=0&linked_partitioning=1&app_version=1630392657&app_locale=en'

#Tom Client ID
# init_url = "https://api-v2.soundcloud.com/search/users?q=hip%20hop%20rap%20repost&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset={}&linked_partitioning=1&app_version=1623250371&app_locale=en"
# profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&sc_a_id=cd72f6993ec796ae3b8a77356b5c7f5a34b1d2b9&variant_ids=&facet=place&user_id=894984-656968-329615-449581&client_id=EQalBjJSm7usfAMYNXh3cHafam0VmNrw&limit=200&offset=0&linked_partitioning=1&app_version=1623250371&app_locale=en'