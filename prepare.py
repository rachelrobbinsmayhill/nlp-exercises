import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire


def basic_clean(string):
    '''
    This function takes in a string, applies basic text cleaning to it,
    then returns normalized text, making all text lowercase, normalizing unicode characters,
    and replacing anything that is not a letter, number, whitespace, or a single quote.
    '''
    # removes accented characters; removes inconsistencies in unicode, converts resulting 
    # string to ASCII character, while ignoring warnings, and decodes to turn resulting bytes back into string. 
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    # # removes special characters, substituting anything that is NOT a letter, number, apostrophe, or whitespace, 
    # then makes text lowercase
    string = re.sub(r"[^a-z0-9'\s]", '', string).lower()
    return string



def tokenize(string):
    '''
    This function takes in a string and
    tokenizes the string; breaking them down into discrete units.
    '''
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str = True)
    
    return string


def stem(text):
    '''This function accepts text and returns the stemmed text.
    '''
    # create the stemmer
    ps = nltk.porter.PorterStemmer()
    
    # apply the stemming transformation to all the words in the text using split
    stems = [ps.stem(word) for word in text.split()]
    
    # join the list of words into a string again assigned to the variable article_stemmed
    text_stemmed = ' '.join(stems)
    
    return text

def lemmatize(text):
    '''This function takes in a string and returns 
    a string with the words lemmatized.
    '''
    
    # create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()

    lemmas = [wnl.lemmatize(word) for word in text.split()]
    
    text_lemmatized = ' '.join(lemmas)
    
    
    return text


def remove_stopwords(text, extra_words = [], exclude_words = []):
    
    '''
    This function takes in text, optional extra_words and exclude_words
    with default empty lists and returns the text.
    '''
    
    # assign stopwords from nltk into stopword_list
    stopword_list = stopwords.words('english')
    # remove excluded words using set
    stopword_list = set(stopword_list) - set(exclude_words)
    # add extra words to the set using union
    stopword_list = stopword_list.union(set(extra_words))

    # split the text by spaces
    words = text.split()
    # assign filtered words as any word in the text that is not in the stopwords list
    filtered_words = [word for word in words if word not in stopword_list]

    # join the filtered list back with the spaces
    text_without_stopwords = ' '.join(filtered_words)

    print('Removed {} stopwords'.format(len(words) - len(filtered_words)))
    print('---')

    print(text_without_stopwords)
    
    
    return text_without_stopwords


def prep_article_data(df, column, extra_words =[], exclude_words=[]):
    '''
    This function takes in a dataframe, and the string name for a column with an option to
    pass extra_word and exclude_word lists. It returns a dataframe with the text title,
    original text, cleaned text with stop words removed which has had tokenization applied to it, 
    stemmed, text, and lemmatized text.
    '''
    
    df['clean'] = df[column].apply(basic_clean)\
                                   .apply(tokenize)\
                                   .apply (remove_stopwords, 
                                           extra_words = extra_words, 
                                           exclude_words= exclude_words)
    df['stemmed'] = df['clean'].apply(stem)
    df['lemmatized'] = df['clean'].apply(lemmatize)

    return df[['title', column, 'clean', 'stemmed', 'lemmatized']]
    




