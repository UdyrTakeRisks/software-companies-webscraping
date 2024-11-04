import csv
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import re
from urllib.parse import urlparse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# take location name from user
print('\tWELCOME TO GOOGLE WEB SCRAPING FOR SOFTWARE COMPANIES IN EGYPT')

location_name = input('Enter Location Name: ')

query = f'Software+Companies+In+{location_name}'

search_url = f'https://www.google.com/search?sa=X&sca_esv=e3415725a8787c2e&hl=en&biw=960&bih=586&tbs=lf:1,lf_ui:2&tbm=lcl&q={query}&rflfq=1&num=10&ved=2ahUKEwiX5-bpt5WJAxXuVqQEHVahOowQjGp6BAgkEAE'

search_response = requests.get(search_url, headers=headers)

print(search_response)
soup = BeautifulSoup(search_response.content, 'lxml')

# print(soup.prettify())

page_links_markup = soup.find_all('a', {'class': 'fl'})

# print(page_links_markup)

page_links = [search_url]  # initialized with page 1

for page_link in page_links_markup:
    link = page_link.get('href')
    if link:
        page_links.append('https://www.google.com' + link)

# print(page_links[-1]) # get the last page

# page_response = requests.get(page_links[-1], headers=headers)

# page_soup = BeautifulSoup(page_response.content, 'lxml')

# page_hidden_markup = page_soup.find_all('a', {'class': 'fl'})

# print(page_hidden_markup)

# page_hidden_links = []

# for page_hidden_link in page_hidden_markup:
#     link = page_hidden_link.get('href')
#     if link:
#         page_hidden_links.append('https://www.google.com' + link)

# print(page_hidden_links[5:])

# page_links.append(page_hidden_links[5:])

# print(page_links)

names = []
websites = []

for link in page_links:
    link_response = requests.get(link, headers=headers)
    link_soup = BeautifulSoup(link_response.content, 'lxml')
    company_names = link_soup.find_all('div', {'class': 'dbg0pd'})  # ok rllt__details v dbg0pd
    company_websites = link_soup.find_all('a', {'class': 'yYlJEf Q7PwXb L48Cpd brKmxb'})

    for company_name in company_names:
        names.append(company_name.text)

    for company_website in company_websites:
        websites.append(company_website.get('href'))
    
# print(names)

# print(websites)


csv_filename = f'Software Companies In {location_name}.csv'

file_list = [names, websites]
data_exported = zip_longest(*file_list)

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Company', 'Website'])

    csv_writer.writerows(data_exported)
