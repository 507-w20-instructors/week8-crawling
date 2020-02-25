import requests
from bs4 import BeautifulSoup

## Make the soup
url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

## Get the searching-div
searching_div = soup.find(id='searching-the-tree')
#print(searching_div)

## Loop through the child divs, print header
child_divs = searching_div.find_all('div', class_='section', recursive=False)
for c_div in child_divs:
    c_header = c_div.find('h2')
    print(c_header.text)

## Loop through the grandchild divs, print header
    grandchild_divs = c_div.find_all('div', class_='section', recursive=False)
    for g_div in grandchild_divs:
        g_header = g_div.find('h3')
        print('\t', g_header.text)