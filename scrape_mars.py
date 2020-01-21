#Import Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests



#=====================================================================================
def scrape():

    mars_dict = {}

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
    # !which chromedriver

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
    #Mars Facts website
    facts_url = "https://space-facts.com/mars/"

    #Munge Data
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Mars','Info']
    mars_df

    #Set mars_df to html
    mars_html = mars_df.to_html()
    mars_html.replace('\n','')

    mars_df.to_html('mars_table.html')

#=====================================================================================
    #Master Lists
    title_list = []
    url_list = []

    #Cerberus Hemi 
    c_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"

    c_html = requests.get(c_url)

    #Hemi BeautifulSoup
    c_soup = bs(c_html.text,'html.parser')

    #Pull title and image
    cerb_site = c_soup.find_all('div',{'class':'container'})

    for ct in cerb_site:
        cerb_img_url = ct.find('img',{'class':'wide-image'})['src']
        cerb_title = ct.find('h2',{'class':'title'})
        
        title_list.append(cerb_title.text)
        url_list.append(c_url + cerb_img_url)
    
    #Schiaparelli URL
    s_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"

    s_html = requests.get(s_url)

    #Schiaparelli BeautifulSoup
    s_soup = bs(s_html.text,'html.parser')

    #Pull title and image
    schi_site = s_soup.find_all('div',{'class':'container'})

    for st in schi_site:
        schi_image_url = st.find('img',{'class':'wide-image'})['src']
        schi_title = st.find('h2',{'class':'title'})
        
        url_list.append(s_url + schi_image_url)
        title_list.append(schi_title.text)
        
    #Syrtis URL
    sy_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"

    sy_html = requests.get(sy_url)

    #Syrtis BeautifulSoup
    sy_soup = bs(sy_html.text, 'html.parser')

    #Pull title and image
    sy_site = sy_soup.find_all('div',{'class':'container'})

    for syt in sy_site:
        sy_img_url = syt.find('img',{'class':'wide-image'})['src']
        sy_title = syt.find('h2',{'class':'title'}).text
        
        title_list.append(sy_title)
        url_list.append(sy_url + sy_img_url)

    #Valles URL
    v_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"

    v_html = requests.get(v_url)

    #Valles BeautifulSoup
    v_soup = bs(v_html.text, 'html.parser')

    v_site = v_soup.find_all('div', {'class':'container'})

    for vt in v_site:
        v_img_url = vt.find('img', {'class':'wide-image'})['src']
        v_title = vt.find('h2',{'class':'title'}).text
        
        url_list.append(v_url + v_img_url)
        title_list.append(v_title)
        
    #Create Dictionary
    hemi_dict = {'title': title_list,'hemisphere': url_list}
    
#=====================================================================================
    browser.quit()