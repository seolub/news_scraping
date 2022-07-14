'''
Scraping functions
'''
from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd
from pysentimiento import create_analyzer
import json


def get_all_paths(keyword, section):
    '''
    For a certain KEYWORD where el pais has the following structure:
    "https://elpais.com/SECTION/KEYWORD", extract all the article links (paths) of all pages.

    Section can be either "autor" or "noticias".
    '''

    starting_url = "https://elpais.com/" + section + "/" + keyword

    paths = set()
    more_pages = True
    i = 0

    while more_pages:
        request = get_request(starting_url + "/" + str(i))

        if request:
            request_text = read_request_links(request)
            soup = BeautifulSoup(request_text, "html5lib")
            get_all_links_from_page(paths, soup)
            i += 1
            print(i, "pages scraped")
            print(len(paths), "number of paths retrieved")
        else:
            more_pages = False
    
    return paths

    
def scrape_paths(paths, keyword):
    '''
    For a list of paths, get articles information (date, title, author, date), 
    and get sentiment of text. Then export a csv file in the data folder
    '''
    all_news = []
    not_found = []
    i = 0 
    analyzer = create_analyzer(task="sentiment", lang="es")

    for path in paths:
        print("Processing", path)
        url = "https://elpais.com" + path
        request = get_request(url)
        if request:
            request_text = read_request_article(request)
            soup = BeautifulSoup(request_text, "html.parser")
            date, author, title, text = extract_news_info(soup, all_news, True)

            if date:
                year = date[0:4]
                month = date[5:7]
                day = date[8:10]
            
            if text:
                neg, pos, neu = get_text_analytics(analyzer, text)
            else:
                neg = None
                pos = None
                neu = None

            all_news.append([date, author, title, text, path, year, month, day, neg, pos, neu])
            i +=1 
            print(i, "articles processed")
        
        else:
            not_found.append(path)
        
    final = pd.DataFrame(all_news, columns = ["date", "author", "title", "text", 
                                                "path", "year", "month", "day", "neg", "pos", "neu"])
    
    print(len(not_found), "paths not found")
    print(not_found)

    final.to_csv("data/" + keyword + ".csv", encoding='utf-8-sig')




def get_request(url):
    '''
    Read data from url
    '''
    try:
        r = requests.get(url)
        if r.status_code == 404 or r.status_code == 403:
            r = None
    except Exception:
        # fail on any error
        r = None
    return r

def read_request_links(request):
    '''
    Return request to extract links.
    Return None if read fails
    '''
    try:
        return request.text.encode('utf-8')
    except Exception:
        print("read failed: " + request.url)
        return ""

def read_request_article(request):
    '''
    Return request to extract article information. 
    Return None if read fails
    '''
    try:
        return request.content
    except Exception:
        print("read failed:" + request.url)
        return ""

def get_all_links_from_page(paths, soup):
    '''
    Read all relevant links in one page
    '''
    for link in soup.find_all('a'):
        path = link.get('href') 
        if "https" not in path:
            if "html" in path:
                paths.add(path)

def extract_news_info(soup, all_news, json_mode=True):
    '''
    Extract text, date, title and author for one page. Json_mode uses website structure. If 
    False, it extracts information by using substrings (more inefficient).
    '''
    if json_mode:
        if len(soup.select('[type="application/ld+json"]')) > 1:
            ld_json = soup.select('[type="application/ld+json"]')[1]
            data = json.loads(ld_json.text)
            
            if 'articleBody' in data:
                text = data['articleBody']
            else:
                text = None

            if 'datePublished' in data:
                date = data['datePublished']
            else: 
                date = None

            if 'headline' in data:  
                title = data['headline']
            else: 
                title = None

            if 'author' in data:
                author = data['author'][0]['name']
            else:
                author = None

            return date, author, title, text 

        else:
            return "error", "error", "error", "error"

    else:
        s = soup.text
        title_res = re.search('"headline":"(.*)","datePublished"', s)

        if title_res:
            title = title_res.group(1)
        else:
            title = None


        date_res = re.search('"datePublished":"(.*)","dateModified"', s)

        if date_res:
            date = date_res.group(1)
        else:
            date = None


        text_res = re.search('"articleBody":"(.*)","keywords"', s)

        if text_res:
            text = text_res.group(1)
        else:
            text = None

        author_res = re.search('"name":"(.*)"}],"creationDate":', s)

        if author_res:
            author = author_res.group(1)
        else:
            author = None
        
        return date, author, title, text 

def get_text_analytics(analyzer, text):
    '''
    Get sentiment of a text using the pysentimiento library
    '''
    probs = analyzer.predict(text).probas
    neg = probs['NEG']
    pos = probs['POS']
    neu = probs['NEU']

    return neg, pos, neu