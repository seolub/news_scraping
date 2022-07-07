'''
Main Scrape
'''

from resources.functions import get_all_paths
from resources.functions import scrape_paths

keyword = input('Enter Keyword: ')
paths = get_all_paths(keyword)
scrape_paths(paths, keyword)
