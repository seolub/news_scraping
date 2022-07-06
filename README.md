# News Scraping

Author: Sergio Olalla 

This program gives the user the ability to scrape news from El Pais for certain keywords that follow the following format:
https://elpais.com/noticias/<<keyword>>. 

For example https://elpais.com/noticias/europa/

The program retrieves the articles available and returns the following information:
- Date
- Author
- Title
- Text
- Path
- Sentiment Probabilities (from 0 to 1)

The output of the information is stored in the folder "/data"

### Installing the Application

1. Run bash install.sh in the top-level directory, this will install all required libraries in a virtual environment
2. Enter the virtual environment with source news_scraping/bin/activate
3. Launch the dash server with ipython3 larry_on_fire.py and click on the link displayed in the output

### Selecting Keyword

1. Run `ipython3 scrape.py` in the top-level directory
2. Enter a keyword in the command line 
3. View the output of the program in `data/`


