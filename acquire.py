import requests from get
from bs4 import BeautifulSoup
import pandas as pd

def get_one_blog_article(url):
    '''This function takes in a url in string format, it provides a User-Agent to the URL and requests a response using the URL and headers.
    It then uses the BeautifulSoup library to parse the URL contents. Lastly, it creates an empty dictionary, then stores the article title and 
    blog article contents in the dictionary. It returns the dictionary as output.
    '''
    
    headers = {'User-Agent': 'Innis Data Science cohort'} 
    response = get(url, headers=headers)

    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    output = {}
    output['title'] = soup.select_one('h1.entry-title').text
    output['contents'] = soup.select_one('div.entry-content').text
    
    return output    


def get_blog_articles(urls):
    '''This function takes in a list of urls in string format. It applies the get_one_blog_article function above to obtain the title and contents
    of each of the blog urls. It then returns a dataframe with the title and contents. 
    '''
    
    # Create a list of dictionaries
    list_dic = [get_one_blog_article(url) for url in urls] 
    # Return a data frame
    return pd.DataFrame(list_dic).style.set_properties(**{'text-align':'left'})