from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os





def get_one_blog_article(url):
    '''This function takes in a url in string format, it provides a User-Agent to the URL and requests a response using the URL and headers.
    It then uses the BeautifulSoup library to parse the URL contents. Lastly, it creates an empty dictionary, then stores the article title,
    date published,and blog article contents in the dictionary. It returns the dictionary as output.
    '''
    
    headers = {'User-Agent': 'Innis Data Science cohort'} 
    response = get(url, headers=headers)

    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    output = {}
    output['title'] = soup.select_one('h1.entry-title').text
    output['published'] = soup.select_one('.published').text
    output['contents'] = soup.select_one('div.entry-content').text
    
    return output    


urls = [
    'https://codeup.com/codeup-news/codeup-start-dates-for-march-2022/',
    'https://codeup.com/featured/5-books-every-woman-in-tech-should-read/',
    'https://codeup.com/codeup-news/dallas-campus-re-opens-with-new-grant-partner/',
    'https://codeup.com/codeup-news/codeups-placement-team-continues-setting-records/',
    'https://codeup.com/it-training/it-certifications-101/'
]


def get_blog_articles(urls):
    '''This function takes in a list of urls in string format. 
    It applies the get_one_blog_article function above to obtain the title and contents
    of each of the blog urls. It then returns a dataframe with the title and contents. 
    '''
    
    # Create a list of dictionaries
    list_dic = [get_one_blog_article(url) for url in urls] 
    # Return a data frame
    return pd.DataFrame(list_dic)   #.style.set_properties(**{'text-align':'left'})



# Take in ANY card
def parse_news_card(card, category):    
    output = {}
    output['category'] = category
    output['title'] = card.select_one('a.clickable').text.strip()

    card_content = card.select_one('div.news-card-content')
    output['content'] = card_content.select_one('div').text
    output['author'] = card_content.select_one('.author').text
    output['published'] = card_content.select_one('.time').attrs['content']
    
    return output


# Need a function to obtain ANY CATEGORY
# take in a category and returns a list of dictionaries list[dict]
def parse_inshorts_page(category):
    url = 'https://inshorts.com/en/read/' + category
    response = get(url)
    soup = BeautifulSoup(response.text)
    articles = [parse_news_card(card, category) for card in soup.select('.news-card')]
    
    return articles


def get_news_articles():
    categories = ['business', 'sports', 'entertainment', 'technology']
    articles = []

    for category in categories:
        print(f'Getting articles for {category}')
        category_articles = parse_inshorts_page(category)
        articles.extend(category_articles)
    return pd.DataFrame(articles)


