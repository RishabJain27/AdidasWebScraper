# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
client = MongoClient("mongodb+srv://rjain9:Ilikepie16@sneakers.1azjgzw.mongodb.net/?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["adidas"]


aTagsInLi = driver.find_elements("xpath", "//div[@class='glass-product-card-container with-variation-carousel']")
line_items=[]
categoryCounter = 0
for a in aTagsInLi:
    #get site url for each shoe
    siteTag = a.find_element(By.TAG_NAME,'a')
    site = siteTag.get_attribute('href')

    #get img source for each shoe
    imgTag = a.find_element(By.TAG_NAME, 'img')
    image_url = imgTag.get_attribute('src')

    #get name for each shoe
    name = imgTag.get_attribute('alt')

    category = a.find_elements("xpath", "//p[@class='glass-product-card__category']")[categoryCounter].text

    #determine gender
    if "Men" in name:
        gender = "Male"
    elif "Women" in name:
        gender = "Female"
    elif "Children" in name or "Youth" in name or "Infant" in name:
        gender = "Kid"
    else:
        gender = "Unisex"
    
    #create json object for database
    myjson3 = {
                'name': name,
                'image_url': image_url,
                'site': site,
                'category': category,
                'gender': gender,
                'brand' : 'Adidas'
            }
    line_items.append(myjson3)
    categoryCounter = categoryCounter + 1

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)
    




