import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request
import os

def get_information(url):
    information = dict()

    response = requests.get(url)
    html = BS(response.text, "html.parser")

    # print(html)

    title = html.find("span", attrs={"data-test":"title"})
    subtitle = html.find("span", attrs={"data-test":"subtitle"})
    author = html.find("a", attrs={"data-role":"AUTHOR"})

    book_title = title.text
    if subtitle:
        book_subtitle = subtitle.text
    else:
        book_subtitle = ''
    book_author = author.text
    

    raw_specs_list_1 = html.find_all(class_="specs__list")[0].find_all()

    for i in range(len(raw_specs_list_1)):

        if remove_whitepace_dd(raw_specs_list_1[i].text) == "Verschijningsdatum":
            raw_pub_date = remove_whitepace_dd(raw_specs_list_1[i+1].text)
            pub_date_number = ''.join(s for s in raw_pub_date if s.isdigit())
            pub_date_month = ''.join(s for s in raw_pub_date if not s.isdigit())
            book_pub_date = f'{pub_date_month.capitalize()} {pub_date_number}'

        # parse page numbers
        elif remove_whitepace_dd(raw_specs_list_1[i].text) == "Aantalpagina's":
            raw_page_number = remove_whitepace_dd(raw_specs_list_1[i+1].text)
            book_page_numbers = ''.join(s for s in raw_page_number if s.isdigit())
            
    # parse publisher
    raw_specs_list_2 = html.find_all(class_="specs__list")[1].find_all()
    for i in range(len(raw_specs_list_2)):

        if remove_whitepace_dd(raw_specs_list_2[i].text) == "Uitgever":
            raw_book_publisher = remove_whitepace_dd(raw_specs_list_2[i+1].text)

    book_publisher = ' '.join(re.findall('[A-Z][^A-Z]*', raw_book_publisher))

    raw_specs_list_3 = html.find_all(class_="specs__list")[2].find_all()

    for i in range(len(raw_specs_list_3)):
        if remove_whitepace_dd(raw_specs_list_3[i].text) == "EAN":
            book_EAN = remove_whitepace_dd(raw_specs_list_3[i+1].text)

    information['title'] = book_title
    information['subtitle'] = book_subtitle
    information['authors'] = book_author
    information['publisher'] = book_publisher
    information['publication_date'] = book_pub_date
    information['pages'] = book_page_numbers
    information['EAN'] = book_EAN

    img = html.find(attrs={'data-test':'product-image'})

    if img:
        img_url = img['src']
        urllib.request.urlretrieve(img_url, f"book_library/static/book_library/thumbnails/{book_title}.jpg")
    
    return information


def remove_whitepace_dd(dd):

    dd = dd.replace("\n", "")
    stripped = dd.replace(" ", "")
    
    return stripped

# url = "https://www.bol.com/nl/p/gouden-bergen/9200000124091929/?bltgh=oZIf0eSjOQHBpmHMkv1BLw.1_4.6.ProductImage"
url = "https://www.bol.com/nl/f/uncanny-valley/9200000099807607/"

get_information(url)




