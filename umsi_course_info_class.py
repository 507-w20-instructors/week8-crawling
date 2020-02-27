import requests
from bs4 import BeautifulSoup

# Request header
headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
    'From': 'mwnewman@umich.edu', ## please replace with your own email
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}

class UMSICourse:

    # Class constants
    COURSE_DETAILS_DIV_CLASS = 'grid--3col-2'
    NAME_NUMBER_CONTAINER_TAG = 'h1'
    NAME_NUMBER_DIVIDER = '-'
    DESCRIPTION_CONTAINER_TAG = 'p'
    CREDITS_DIV_CLASS = 'credit-hours'
    CREDITS_CONTAINER_TAG = 'span'
    PREREQS_ENFORCED_DIV_CLASS = 'prerequisites-enforced'
    PREREQ_CONTAINER_TAG = 'li'


    def __init__(self, url, details_soup):
        self.url = url
        self.number = self.extract_course_number(details_soup)
        self.name = self.extract_course_name(details_soup)
        self.description = self.extract_description(details_soup)
        self.credits = self.extract_credits(details_soup)
        self.prereqs = self.extract_prereqs(details_soup)


    def extract_course_number_name(self, soup):
        return(soup
            .find(class_=self.COURSE_DETAILS_DIV_CLASS)
            .find(self.NAME_NUMBER_CONTAINER_TAG)
            .text.strip())


    def extract_course_number(self, soup):
        number_name = self.extract_course_number_name(soup)
        return int(number_name
            .split(self.NAME_NUMBER_DIVIDER)[0]
            .strip())


    def extract_course_name(self, soup):
        number_name = self.extract_course_number_name(soup)
        return (number_name
            .split(self.NAME_NUMBER_DIVIDER)[1]
            .strip())


    def extract_description(self, soup):
        desc = (soup
            .find(class_=self.COURSE_DETAILS_DIV_CLASS)
            .find(self.DESCRIPTION_CONTAINER_TAG)
            .text.strip())
        return desc


    def extract_credits(self, soup):
        cred_str = (soup
            .find(class_=self.CREDITS_DIV_CLASS)
            .find(self.CREDITS_CONTAINER_TAG)
            .text.strip())
        return int(cred_str)


    def extract_prereqs(self, soup):
        prereqs = []
        prereqs_div = soup.find(class_=self.PREREQS_ENFORCED_DIV_CLASS)
        if (prereqs_div is not None):
            prereq_items = prereqs_div.find_all(self.PREREQ_CONTAINER_TAG)
            for p in prereq_items:
                prereqs.append(p.text.strip())
        return prereqs


    def __str__(self):
        s = f'{self.number}: {self.name} [{self.credits} credits]'
        s += f'\n{self.description[0:50]}...' 
        s += f'\nPrereqs: '
        if len(self.prereqs) == 0:
            s += f'None'
        else:
            s += ','.join(self.prereqs)
        return s


def build_course(course_url):
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
    UMSICourse
        An instance of a UMSI course, built from course_url
    '''

    response = requests.get(course_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return UMSICourse(course_url, soup)


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
            value=UMSICourse object
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

        course = build_course(course_details_url)
        courses[course.number] = course

    return courses


if __name__ == '__main__':

    courses = build_course_dictionary()

    print('-' * 40)
    for k in courses.keys():
        print(courses[k])
        print('-' * 40)



