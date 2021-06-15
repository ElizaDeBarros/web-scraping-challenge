# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import warnings
warnings.filterwarnings('ignore')


def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dic = {}

    #Scrape the [Mars News Site](https://redplanetscience.com/)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)
    html=browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Collect the latest News Title and Paragraph Text
    latest_news_title=soup.find_all('div', class_='content_title')
    latest_news_title = latest_news_title[0].text
    paragraph_latest_news_title=soup.find_all('div', class_='article_teaser_body')
    paragraph_latest_news_title = paragraph_latest_news_title[0].text
    
 

    # Visit the url for the Featured Space Image site (https://spaceimages-mars.com)
    url_jpl = 'https://spaceimages-mars.com'
    browser.visit(url_jpl)
    time.sleep(2)
    html_img=browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup_img = bs(html_img, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string
    # to a variable called `featured_image_url`

    images = soup_img.find_all('img', class_='headerimage fade-in')
    for image in images:
        featured_image_url = (image['src'])

    featured_image_url ='https://spaceimages-mars.com/' + featured_image_url
    

    # Visit the Mars Facts webpage (https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about
    # the planet including Diameter, Mass, etc
    url_facts = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url_facts)
    df = table[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index("Description", inplace=True)

    # Use Pandas to convert the data to a HTML table string.
    html_table=df.to_html(classes='table table-striped')
        

    # Visit the astrogeology site(https://marshemispheres.com/) to obtain high resolution images for each of Mar's hemispheres.
    url_hemisp = 'https://marshemispheres.com/'
    response = requests.get(url_hemisp)
    soup_hemisp = bs(response.text, 'html.parser')

    links=[]
    results = soup_hemisp.find_all('div', class_='description')

    for result in results:
        to_visit = result.find('a','href', class_='itemLink product-item')['href']
        
        # visit hemisphere page
        browser.visit(f'{url_hemisp}{to_visit}')
        
        # create a soup object for the page being visited
        html_img = browser.html
        soup_ind = bs(html_img, 'html.parser')
        
        image_links = soup_ind.find('div', class_='wrapper')
        image_links = image_links.find('img',class_='wide-image')["src"]
        image_links = f'https://marshemispheres.com/{image_links}'
        
        title = soup_ind.find('h2',class_='title').text
        links.append({'title':title,'img_url':image_links})
        
        try:
            browser.links.find_by_text('back').click()
            
        except:
            pass
            

    mars_dic = {'latest_news_title': latest_news_title, 'paragraph_latest_news_title' : paragraph_latest_news_title,
            'featured_image_url': featured_image_url,'html_table': html_table,'links': links}

    browser.quit()
    return mars_dic
