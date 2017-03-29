import requests
from bs4 import BeautifulSoup
import string

def open_url(url):
    """opens url and returns a soup object"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_id(link, start):
    string = link
    end = '&'
    id = string[string.find(start) + len(start):string.find(end)]
    return id

def cleaner(name):
    clean_name= "".join(l for l in name if l not in string.punctuation)
    return clean_name
def remove_(a):
    a_ = a.replace("'", "")
    return(a_)