import requests
from bs4 import BeautifulSoup
import time
import json

BASE_URL = 'https://www.si.umich.edu'
COURSES_PATH = '/programs/courses'
CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'mwnewman@umich.edu', ## please replace with your own email
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}


def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]


## Load the cache, save in global variable
CACHE_DICT = load_cache()

## Make the soup for the Courses page
courses_page_url = BASE_URL + COURSES_PATH
url_text = make_url_request_using_cache(courses_page_url, CACHE_DICT)
soup = BeautifulSoup(url_text, 'html.parser')

## For each course listed
course_listing_parent = soup.find('div', class_='item-teaser-group')
course_listing_divs = course_listing_parent.find_all('div', recursive=False)
for course_listing_div in course_listing_divs:

    ## extract the course details URL
    course_link_tag = course_listing_div.find('a')
    course_details_path = course_link_tag['href']
    course_details_url = BASE_URL + course_details_path

    ## Make the soup for course details
    url_text = make_url_request_using_cache(course_details_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')

    ## extract course number and name
    number_name = soup.find(class_='grid--3col-2').find('h1')
    print(number_name.text.strip())

    ## extract course description
    desc = soup.find(class_='grid--3col-2').find('p')
    print(desc.text.strip()[0:50], '...')

    ## extract credit hours
    credits = soup.find(class_='credit-hours').find('span')
    print('Credits:', credits.text.strip())

    ## extract prereqs
    prereqs_div = soup.find(class_='prerequisites-enforced')
    if (prereqs_div is not None):
        prereqs = prereqs_div.find_all('li')
        for p in prereqs:
            print('Prereq:', p.text.strip())

    print('-' * 40)




