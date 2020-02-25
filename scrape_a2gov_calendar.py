### UNFINISHED ATTEMPT 
### goal: scrape event details from the a2gov calendar 

import requests
from bs4 import BeautifulSoup

def print_event_details(date_string, event_details_url):
    response = requests.get(event_details_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    location_tag = soup.find('a', class_='calendartext')
    try:
        print('\t', location_tag.text)
    except:
        print('no a+calendartext tag found:')
        print(soup)


base_url = 'https://calendar.a2gov.org/'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

calendar_cells = soup.find_all('td', class_='calendarcell')
for date in calendar_cells:
    date_tag = date.find('h3')
    date_string = date_tag.text
    events = date.find_all('a', class_='url')
    for e in events:
        print_event_details(date_string, base_url + e['href'])
    

