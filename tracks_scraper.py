import os
from resources import get_endless_scroll_content

urls = []
if not os.path.exists('tracks_scraper/rapper_urls.txt'):
    print("Create rapper_url.txt!!!")
else:
    with open('tracks_scraper/rapper_urls.txt', 'r', encoding='utf-8') as f:
        for item in f:
            urls.append(item.strip())

# songlinks = []
for url in urls:
    path = url + "/tracks"
    print("Getting endless scroll content...")
    soup = get_endless_scroll_content(path)
    print("Searching for the songlinks...")
    titles = soup.find_all(class_='soundTitle__title')
    for title in titles:
        with open('tracks_scraper/song_links.txt', 'a', encoding='utf-8') as f:
            f.write('https://soundcloud.com/' + title.attrs['href'])
            f.write('\n')

print("songlinks successfully written")
