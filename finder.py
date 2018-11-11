from datascience import *
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
#import pandas as pd
#import IPython
#import scipy
plt.style.use('fivethirtyeight')
import requests
from bs4 import BeautifulSoup
import time


def craigslist_titles(search):
    url = 'https://sandiego.craigslist.org/search/sss?sort=date&query=' + search
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    result_title_html = soup.findAll('a', attrs={'class': 'result-title hdrlnk'})
    result_titles = make_array()
    for text in result_title_html:
        result_titles = np.append(result_titles, text.get_text())
    return result_titles


def ebay_titles(search):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + search + '&_sacat=0'
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    result_title_html = soup.findAll('h3', attrs={'class': 's-item__title'})
    result_titles = make_array()
    for text in result_title_html:
        if 'SPONSORED' in text.get_text():
            pass
        else:
            result_titles = np.append(result_titles, text.get_text())
    return result_titles


# def new_titles(search):
#     craigslist_updated_titles = craigslist_titles(search)
#     ebay_updated_titles = ebay_titles(search)

def print_listings(titles):
    for each in titles:
        print(each)


def updated_check(titles, updated_titles):
    if titles[0] != updated_titles[0]:
        return True
    else:
        return False


def new_listing_output(titles, updated_titles):
    new_listings = make_array()
    if updated_check(titles, updated_titles):
        for new in updated_titles:
            if new != titles[0]:
                new_listings = np.append(new_listings, new)
    return new_listings

exit = False

search_query = input('Enter what you are looking for: ')

#craigslist_initial_titles = craigslist_titles(search_query)
ebay_initial_titles = ebay_titles(search_query)

while not exit:
    #print_listings(craigslist_initial_titles)
    print(ebay_initial_titles)

    time.sleep(3)

    #craigslist_updated_titles = craigslist_titles(search_query)
    ebay_updated_titles = ebay_titles(search_query)
    ebay_updated_titles = np.concatenate((make_array('wassup'), ebay_updated_titles))
    # print(ebay_updated_titles)

    #print_listings(new_listing_output(craigslist_initial_titles, craigslist_updated_titles))
    print(new_listing_output(ebay_initial_titles, ebay_updated_titles))

    #craigslist_initial_titles = craigslist_updated_titles
    ebay_initial_titles = ebay_updated_titles

    exit = True