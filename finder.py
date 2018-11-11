from datascience import *
import numpy as np
import requests
from bs4 import BeautifulSoup
import time


def craigslist_titles_array(search):
    url = 'https://sandiego.craigslist.org/search/sss?sort=date&query=' + search
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    result_title_html = soup.findAll('a', attrs={'class': 'result-title hdrlnk'})
    result_titles = make_array()
    for text in result_title_html:
        result_titles = np.append(result_titles, text.get_text())
    return result_titles


def ebay_titles_array(search):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + search + '&_sacat=0'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    result_title_html = soup.findAll('h3', attrs={'class': 's-item__title'})
    result_titles = make_array()
    for text in result_title_html:
        if 'SPONSORED' in text.get_text():
            pass
        else:
            if 'New Listing' in text.get_text():
                result_titles = np.append(result_titles, text.get_text()[11:])
            else:
                result_titles = np.append(result_titles, text.get_text())
    return result_titles


def print_listings(titles):
    if titles is not None:
        for each in titles:
            print(each)


def updated(titles, updated_titles):
    if titles[0] != updated_titles[0]:
        return True
    else:
        return False


def new_listing_output(titles, updated_titles):
    new_listings = make_array()
    i = 0
    while updated_titles.item(i) != titles.item(0):
        new_listings = np.append(new_listings, updated_titles.item(i))
        i += 1
        if updated_titles.item(i) == titles.item(0):
            return new_listings


exit = False

search_query = input('Enter what you are looking for: ')

craigslist_titles = craigslist_titles_array(search_query)
ebay_initial_titles = ebay_titles_array(search_query)

print('\nCraigslist Listings: \n')
print_listings(craigslist_titles)
time.sleep(2)
print('\n\nEbay Listings: \n')
print_listings(ebay_initial_titles)

print('\nNew listings will refresh every 10 minutes')

while not exit:
    time.sleep(10*60)

    craigslist_updated_titles = craigslist_titles_array(search_query)
    ebay_updated_titles = ebay_titles_array(search_query)

    if updated(craigslist_titles, craigslist_updated_titles) or updated(ebay_initial_titles, ebay_updated_titles):
        print('\n\nNew Listings: ')
        print_listings(new_listing_output(craigslist_titles, craigslist_updated_titles))
        print_listings(new_listing_output(ebay_initial_titles, ebay_updated_titles))

        craigslist_titles = craigslist_updated_titles
        ebay_initial_titles = ebay_updated_titles
