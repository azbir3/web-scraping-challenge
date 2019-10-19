# coding: utf-8

# # Step 1 - Scraping

# modules and dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import time 
import pandas as pd
import numpy as np

#Set up splinter
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}

# ### NASA MARS News
    # visit URL of page to be scraped
    url_NASA_news = 'https://mars.nasa.gov/news'
    browser.visit(url_NASA_news)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #see image in screenshots folder for determination of "div class"

    # find title of the latest news article from NASA Mars news site
    news_title = soup.find_all('div', class_='content_title')
    # find paragraph out of the latest news article from NASA Mars news site
    news_p = soup.find_all('div', class_='article_teaser_body')

    # add lestest news title and paragrph to the dictionary
    mars_data['news_title']=news_title[0].text
    mars_data['news_p']=news_p[0].text

# ### JPL Mars Space Images - Featured Image

    # visit URL of page to be scraped
    url_space_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_space_image)
    
    # Find and click the "full image" button
    browser.click_link_by_id('full_image')
    time.sleep(1)

    #find a click "more info" button
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    #find the image and then extract the url
    image = image_soup.find('figure', class_='lede')
    image_url=image.find('img')['src']
    
    #Build the url
    featured_image_url= 'https://www.jpl.nasa.gov' + image_url 

    print(featured_image_url )
    # add lestest featured image url to the dictionary
    mars_data['featured_image_url']=featured_image_url

# ### Mars Weather

    # Visit url to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    #find current weather tweet text
    weather = weather_soup.find('div', class_='js-tweet-text-container')
    mars_weather= weather.p.text
    
    print(mars_weather)
    # add lestest featured image url to the dictionary
    mars_data['mars_weather']=mars_weather

# ### Mars Facts

    #url to be scraped
    facts_url='https://space-facts.com/mars/'  

    #retrieve facts table for mars only
    table_of_facts=pd.read_html(facts_url)[1]

    # assign column titles
    table_of_facts.columns=['Description', 'Value']

    # set 'Description' col as index
    table_of_facts.set_index("Description", inplace = True)
    
    # Convert the data to HTML table string
    mars_facts_html = table_of_facts.to_html()
    
    #clean up the table
    mars_facts_html.replace('\n', '')

    #save the table into html file
    mars_data['mars_facts_html']=mars_facts_html

# ### Mars Hemispheres

    # Visit URL of page to be scraped
    url_USGSA = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_USGSA)

    # Create an empty list to hold dictionaries of hemisphere title with the image url string
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css("h3")

    # Loop through those links to find title and href and sore in the dictionary
    for i in range(len(links)):
        # create a dictionary to store retrieved data
        hemisphere = {}
        
        # find css for the link-header and click it
        browser.find_by_css("h3")[i].click()
        
        # Find Hemisphere title and strip it of extra text
        hemisphere['title'] = browser.find_by_css("h2.title").text.replace(" Enhanced", "")
        
        # Find text Sample associated with the image and extract the href
        hemisphere['img_url'] =browser.find_link_by_text('Sample').first['href']
        
        # Append title and url stored in hemisphere to a list
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate back to loop again
        browser.back()
        
    # add hemisphere urls to the dictionary
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()
    return mars_data