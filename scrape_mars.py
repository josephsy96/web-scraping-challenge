#Import Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def scrape():

    #Website to scrape
    mission_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    mission_html = requests.get(mission_url)

    #BS module
    mission_soup = bs(mission_html.text,'html.parser')

    #Variable to iterate through the website
    mars_t = mission_soup.find_all('div', {'class':'content_title'})
    mars_p = mission_soup.find_all('div', {'class':'rollover_description'})

    title = []
    para = []

    #Append data into lists
    for mt in mars_t:
        
        mars_title = mt.find('a').text
        title.append(mars_title)

    for mp in mars_p:
        mars_para = mp.find('div',{'class':'rollover_description_inner'}).text
        para.append(mars_para)