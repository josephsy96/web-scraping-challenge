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

#=====================================================================================
    !which chromedriver

    #Browser elements
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    browser = Browser('chrome', **executable_path, headless=False)

    #URL Info
    splinter_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(splinter_url)

    #Setup pull points
    splinter_html = browser.html

    splinter_soup = bs(splinter_html, 'html.parser')
    jpl_url = []

    art = splinter_soup.select_one('article[class="carousel_item"]')

    #Grab url
    featured_image_url = art['style'].split("url('")[1][:-3]
    jpl_url.append(splinter_url + featured_image_url)

#=====================================================================================
    #Mars Twitter Page
    url = "https://twitter.com/marswxreport?lang=en"

    html = requests.get(url)

    #Soup module
    soup = bs(html.text,'html.parser')

    #Find list items
    mars_tweets = soup.find_all("li", class_="js-stream-item")
    mars_weather = []

    for tweets in mars_tweets:
        rt = tweets.find('p',class_='tweet-text').text.strip().split('pic*')[0][:-26]
        
        mars_weather.append(rt)

    only_weather = [m for m in mars_weather if "InSight" in m]
    fwt = only_weather[0]
    
#=====================================================================================