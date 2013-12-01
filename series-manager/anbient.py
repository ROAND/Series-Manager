import bs4
from bs4 import BeautifulSoup
import sys
import os
import urllib2
import socket
timeout = 10
socket.setdefaulttimeout(timeout)

page = urllib2.urlopen("http://www.anbient.net/tv")
soup = BeautifulSoup(page.read())
number = 0
def get_animes():
    animes = {}
    for div in soup.find_all('div', {'class':'views-field-title'}):
        if isinstance(div, bs4.element.Tag):
            for span in div.children:
                if isinstance(span, bs4.element.Tag):
                    for a in span.children:
                        anime_link = 'http://www.anbient.net'+a['href']
                        anime_name = a.string
                        animes[anime_name] = anime_link
    return animes
animes = get_animes()

for anime in animes.items():
    anime_page = urllib2.urlopen(anime[1])
    anime_soup = BeautifulSoup(anime_page.read())
    #anime_page = urllib2.urlopen(anime.key)
