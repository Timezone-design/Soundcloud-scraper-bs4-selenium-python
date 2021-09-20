from selenium.webdriver.chrome.options import Options
import re

SCROLL_THRESHOLD = 500
DRIVER_PATH = 'chromedriver.exe'
DRIVER_OPTIONS = Options()
DRIVER_OPTIONS.headless = True
DRIVER_OPTIONS.add_argument('--log-level=3')
INSTAGRAM_USERNAME_REGEX = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

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