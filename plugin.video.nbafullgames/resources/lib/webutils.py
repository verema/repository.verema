try:
	from BeautifulSoup import BeautifulSoup as bs
except:
	from bs4 import BeautifulSoup as bs
from modules import client

def read_url(url):
    return client.request(url)

def get_soup(url):
	return bs(read_url(url))

