#!/bin/bash
echo -e "Installing the virtual environment..."
python3 -m venv news_scraping
source news_scraping/bin/activate
pip3 install -r requirements.txt
deactivate
echo -e "Virtual environment is ready!"