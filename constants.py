from selenium.webdriver.chrome.options import Options
import re

SCROLL_THRESHOLD = 500
DRIVER_PATH = 'chromedriver.exe'
DRIVER_OPTIONS = Options()
DRIVER_OPTIONS.headless = True
DRIVER_OPTIONS.add_argument('--log-level=3')
DRIVER_OPTIONS.add_argument("--window-size=1920x1080")
INSTAGRAM_USERNAME_REGEX = re.compile(r'^(instagram|I\.?G\.?)\s?:?\s?@?(.*((-|_).*)?\s?)$', re.IGNORECASE)

init_url = "https://api-v2.soundcloud.com/search/users?q=hip-hop%20rap%20repost&sc_a_id=9b54e44da7a0d8107ba6a6a02735786f3e030fb6&variant_ids=&facet=place&user_id=212832-727922-185643-279192&client_id=bhdPp0QME8kXmKrbDc4gARDVv1v8JNQ3&limit=200&offset={}&linked_partitioning=1&app_version=1627651107&app_locale=en"
profile_search_api = 'https://api-v2.soundcloud.com/search/users?q={}&variant_ids=&facet=place&user_id=339301-954310-146236-973280&client_id=2FBT7dRlnJnnGKXjivkUCFLmzLG80Rur&limit=200&offset=0&linked_partitioning=1&app_version=1630392657&app_locale=en'
