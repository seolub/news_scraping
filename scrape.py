'''
Main Scrape
'''

from resources.functions import get_all_paths
from resources.functions import scrape_paths

section = input('Enter Section (autor OR noticias): ')

if section not in ['noticias', 'autor']:
    raise TypeError("Only 'noticias' or 'autor' is allowed")

keyword = input('Enter Keyword: ')

paths = get_all_paths(keyword, section)
scrape_paths(paths, keyword)
