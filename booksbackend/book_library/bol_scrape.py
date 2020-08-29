import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request
import os
import json

def get_information(url):
    information = dict()

    response = requests.get(url)
    html = BS(response.text, "html.parser")

    json_script = html.find_all("script", attrs={"type":"application/ld+json"})
    
    json_book = json.loads(json_script[-1].string)

    
    book_title = json_book['name']

    subtitle = html.find("span", attrs={"data-test":"subtitle"})
    if subtitle:
        book_subtitle = subtitle.text
    else:
        book_subtitle = ""
    
    try:
        book_author = json_book['author']['name']
    except:
        book_author = json_book['brand']['name']

    try:
        book_publisher = json_book['publisher']['name']
    except:
        backup_div = html.find("div", attrs={"data-test":"taxonomy_data"})
        backup_json = json.loads(backup_div.text)
        print(backup_json)
        book_publisher = backup_json['pdpTaxonomyObj']['productInfo'][0]['publisher']

    try:
        book_pub_date = json_book['workExample']['datePublished']
    except:
        book_pub_date = json_book['releaseDate']

    try:
        book_isbn = json_book['workExample']['isbn']
    except:
        book_isbn = json_book['gtin13']
    

    book_img = json_book['image']['url']
    
    information['title'] = book_title
    information['subtitle'] = book_subtitle
    information['author'] = book_author
    information['publisher'] = book_publisher
    information['publication_date'] = book_pub_date
    # information['pages'] = book_page_numbers
    information['isbn'] = book_isbn

    if book_img:
        urllib.request.urlretrieve(book_img, f"book_library/static/book_library/thumbnails/{book_title}.jpg")
        
    return information


# def remove_whitepace_dd(dd):

#     dd = dd.replace("\n", "")
#     stripped = dd.replace(" ", "")
    
#     return stripped

# url = "https://www.bol.com/nl/p/gouden-bergen/9200000124091929/?bltgh=oZIf0eSjOQHBpmHMkv1BLw.1_4.6.ProductImage"
# url = "https://www.bol.com/nl/f/uncanny-valley/9200000099807607/"
# url = "https://www.bol.com/nl/p/de-prooi/9200000072838235/?bltgh=iwlEjT4lH-OiQTsSCxlF9Q.1_4.5.ProductTitle"

# get_information(url)





