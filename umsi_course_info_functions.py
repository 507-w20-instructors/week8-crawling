import requests
from bs4 import BeautifulSoup
import time

# HTML constants
COURSE_DETAILS_DIV_CLASS = 'grid--3col-2'
NAME_NUMBER_CONTAINER_TAG = 'h1'
NAME_NUMBER_DIVIDER = '-'
DESCRIPTION_CONTAINER_TAG = 'p'
CREDITS_DIV_CLASS = 'credit-hours'
CREDITS_CONTAINER_TAG = 'span'
PREREQS_ENFORCED_DIV_CLASS = 'prerequisites-enforced'
PREREQ_CONTAINER_TAG = 'li'

# Course record constants
COURSE_URL_KEY = 'url'
COURSE_NUMBER_KEY = 'number'
COURSE_NAME_KEY = 'name'
COURSE_DESCRIPTION_KEY = 'description'
COURSE_CREDITS_KEY = 'credits'
COURSE_PREREQS_KEY = 'prereqs'

# Request header
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'mwnewman@umich.edu', ## please replace with your own email
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}


def extract_course_number_name(soup):
    return(soup
        .find(class_=COURSE_DETAILS_DIV_CLASS)
        .find(NAME_NUMBER_CONTAINER_TAG)
        .text.strip())


def extract_course_number(soup):
    number_name = extract_course_number_name(soup)
    return int(number_name
        .split(NAME_NUMBER_DIVIDER)[0]
        .strip())


def extract_course_name(soup):
    number_name = extract_course_number_name(soup)
    return (number_name
        .split(NAME_NUMBER_DIVIDER)[1]
        .strip())


def extract_description(soup):
    desc = (soup
        .find(class_=COURSE_DETAILS_DIV_CLASS)
        .find(DESCRIPTION_CONTAINER_TAG)
        .text.strip())
    return desc


def extract_credits(soup):
    cred_str = (soup
        .find(class_=CREDITS_DIV_CLASS)
        .find(CREDITS_CONTAINER_TAG)
        .text.strip())
    return int(cred_str)


def extract_prereqs(soup):
    prereqs = []
    prereqs_div = soup.find(class_=PREREQS_ENFORCED_DIV_CLASS)
    if (prereqs_div is not None):
        prereq_items = prereqs_div.find_all(PREREQ_CONTAINER_TAG)
        for p in prereq_items:
            prereqs.append(p.text.strip())
    return prereqs


def course_record_to_string(course_record):
    s = f'{course_record[COURSE_NUMBER_KEY]}: '
    s += f'{course_record[COURSE_NAME_KEY]} '
    s += f'[{course_record[COURSE_NUMBER_KEY]} credits]'
    s += f'\n{course_record[COURSE_DESCRIPTION_KEY][0:50]}...' 
    s += f'\nPrereqs: '
    prereqs = course_record[COURSE_PREREQS_KEY]
    if len(prereqs) == 0:
        s += f'None'
    else:
        s += ','.join(prereqs)
    return s


def build_course_record(course_url):
    '''
    scrapes an individual course page 
    (e.g., https://www.si.umich.edu/programs/courses/106), 
    and builds a UMSICourse object
    
    Params
    ------
    course_url: string
        The course details page for the course to build

    Returns
    -------
    dictionary of the form
        { 
            url: <string>, 
            number: <int>,
            name: <string>,
            description: <string>,
            credit_hours: <int>,
            prereqs: [<string>, ...]
        }
    '''

    response = requests.get(course_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_record = {}
    course_record[COURSE_URL_KEY] = course_url
    course_record[COURSE_NUMBER_KEY] = extract_course_number(soup)
    course_record[COURSE_NAME_KEY] = extract_course_name(soup)
    course_record[COURSE_DESCRIPTION_KEY] = extract_description(soup)
    course_record[COURSE_CREDITS_KEY] = extract_credits(soup)
    course_record[COURSE_PREREQS_KEY] = extract_prereqs(soup)
    return course_record

def build_course_dictionary():
    '''
    scrapes https://www.si.umich.edu/programs/courses and builds
    a dictionary of all classes found there

    Params
    ------
    none

    Returns
    -------
    dict
        a dictionary with 
            key=course number
            value=a dictionary of the form
                { 
                    url: <string>, 
                    number: <int>,
                    name: <string>,
                    description: <string>,
                    credit_hours: <int>,
                    prereqs: [<string>, ...]
                }
    '''
    
    BASE_URL = 'https://www.si.umich.edu'
    COURSES_PATH = '/programs/courses'

    COURSE_LISTING_DIV_CLASS = 'item-teaser-group'

    courses = {}

    courses_page_url = BASE_URL + COURSES_PATH
    response = requests.get(courses_page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    course_listing_parent = soup.find(class_=COURSE_LISTING_DIV_CLASS)
    course_listing_divs = course_listing_parent.find_all(
        'div', recursive=False)

    for course_listing_div in course_listing_divs:

        course_link_tag = course_listing_div.find('a')
        course_details_path = course_link_tag['href']
        course_details_url = BASE_URL + course_details_path

        course_record = build_course_record(course_details_url)
        courses[course_record[COURSE_NUMBER_KEY]] = course_record

        #time.sleep(1)

    return courses


if __name__ == '__main__':

    courses = build_course_dictionary()

    print('-' * 40)
    for k in courses.keys():
        print(course_record_to_string(courses[k]))
        print('-' * 40)



