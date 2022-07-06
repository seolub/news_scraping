#!/bin/bash
echo -e "Creating new virtual environment..."
python3 -m venv news_scraping
echo -e "Installing Requirements..."
source news_scraping/bin/activate
pip3 install -r requirements.txt

echo -e "Virtual environment is ready!"

echo -e "Starting application."
python3 scrape.py