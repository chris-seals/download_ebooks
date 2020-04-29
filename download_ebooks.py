#!/usr/bin/env python
# coding: utf-8

# # Bulk download of ebooks


import requests
from bs4 import BeautifulSoup
import re


# #### Change home_dir variable to the destination path
home_dir = '.'


target = r'https://towardsdatascience.com/springer-has-released-65-machine-learning-and-data-books-for-free-961f8181f189'


page_html = requests.get(target)
soup = BeautifulSoup(page_html.content, 'lxml')


book_urls = []
for link in soup.findAll('a', attrs={'href': re.compile("^http://link.springer.com")}):
    book_urls.append(link.get('href'))


for link in book_urls:
    try:
        link_html = requests.get(link)
        link_soup = BeautifulSoup(link_html.content, 'lxml')
        page_headers = link_soup.find_all('div', attrs={'class':'page-title'})
        book_title = [item.find('h1').text for item in page_headers][0]
        full_book_link = link_soup.find_all('a', attrs={'title': re.compile("Download this book")})
        url = full_book_link[0].get('href')
        book = requests.get(f'http://link.springer.com{url}', allow_redirects=True)
        with open (f'{home_dir}/{book_title}.pdf', 'wb') as f:
            f.write(book.content)
        print(f'{book_title} downloaded successfully')
    except Exception as e:
        print(e)

