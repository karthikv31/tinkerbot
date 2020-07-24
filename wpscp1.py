import os
import re
from urllib.request import urlopen
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
import requests

BLOG2_SCRAPE = ''
POSTLINK = 'https://wordpress.com/block-editor/post/tinkerbotblog.wordpress.com/31'

def scrape_link():
    """Get the text body and images of links."""
    ht_ml = urlopen(POSTLINK)
    b_s = BeautifulSoup(ht_ml.read(), 'lxml')

    with open('image_links.txt', 'a', encoding='utf-8') as file:

        png_images = b_s.find_all('img', {'src':re.compile('.png')})
        for image in png_images:
            image_link = (image['src'])
            print(image_link)
            file.write((image['src']))
            file.write('\n\n')

    so_up = b_s.find_all('div', {'class':''})

    if not so_up:
        so_up = b_s.find_all('div', {'class':'block-list-appender'})


def create_folder():
    """Create a folder using blog name."""
    my_dir = (str(BLOG2_SCRAPE))
    my_dir = my_dir[: my_dir.find('.wordpress')]
    my_dir = my_dir.replace('https://', '')

     # If it doesn't exist then create it.
    check_folder = os.path.isdir(my_dir)
    if not check_folder:
        os.makedirs(my_dir)
        print('created folder : ' +my_dir)

    # Change dir to new folder.
    os.chdir(my_dir)

def scrape_sitemap():
    """Get all links from url (BLOG2_SCRAPE) via the sites sitemap.xml."""
    pa_ges = []

    req_uest = str(BLOG2_SCRAPE)+'sitemap.xml'
    f_w = urlopen(req_uest, timeout=3)
    xm_l = f_w.read()

    so_up = BeautifulSoup(xm_l, 'xml')
    url_tags = so_up.find_all('url')

    
    # Save urls to a text file named links.txt to curr dir.
    with open('links.txt', 'w') as file:
        for sitemap in url_tags:
            link = sitemap.findNext('loc').text
            pa_ges.append(link)
            file.write(link)
            file.write('\n')
    f_w.close()

BLOG2_SCRAPE = 'https://wordpress.com/block-editor/post/tinkerbotblog.wordpress.com/31'

# Main.
create_folder()


#open text file of scraped links
#and call scrape_link for each link

with open('links.txt', encoding='utf-8') as f:
    for line in f:
        POSTLINK = line
        print(POSTLINK)
        scrape_link()

print()
print()
print("Finished Scrape.")
