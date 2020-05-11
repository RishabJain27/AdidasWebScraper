# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from pymongo import MongoClient
import sys
import time
sys.stdout = open('file', 'w', encoding="utf-8")

url = "https://www.adidas.com/us/shoes-new_arrivals"

# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

# get web page
driver.get(url)

driver.maximize_window()
time.sleep(5)

# execute script to slowly scroll down the page
len = 7333
scrollVal = 250
while scrollVal <= len:
    driver.execute_script("scrollBy(0,250);")
    scrollVal = scrollVal + 250


#connect to database
client = MongoClient("mongodb+srv://rjain9:Ilikepie16%21@cluster0-wgm3y.mongodb.net/test?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["adidas"]


aTagsInLi = driver.find_elements_by_class_name('grid-item___eaXVb')
line_items=[]
for a in aTagsInLi:
    #get site url for each shoe
    siteTag = a.find_element_by_tag_name('a')
    site = siteTag.get_attribute('href')

    #get img source for each shoe
    imgTag = a.find_element_by_tag_name('img')
    image_url = imgTag.get_attribute('src')
    print(image_url)

    #get name for each shoe
    name = imgTag.get_attribute('title')

    #get category
    category = a.find_element_by_class_name('gl-product-card__category').text
    print(category)

    #determine gender
    if "Men" in category:
        gender = "Male"
    elif "Women" in category:
        gender = "Female"
    elif "Children" in category or "Youth" in category or "Infant" in category:
        gender = "Kid"
    else:
        gender = "Unisex"

    #create json object for database
    myjson3 = {
                'name': name,
                'image_url': image_url,
                'site': site,
                'category': category,
                'gender': gender
            }
    line_items.append(myjson3)

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)
    




