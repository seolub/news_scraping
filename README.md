# News Scraping

Author: Sergio Olalla 

This program gives the user the ability to scrape news from El Pais for certain keywords that follow the following format:
https://elpais.com/noticias/<<keyword>> or https://elpais.com/autor/<<keyword>>

For example https://elpais.com/noticias/europa/ or https://elpais.com/autor/victor-lapuente-gine

The program retrieves the articles available and returns the following information:
- Date
- Author
- Title
- Text
- Path
- Sentiment Probabilities (from 0 to 1)

The output of the information is stored in the folder "/data"

### Installing the Requirements

1. Run bash install.sh in the top-level directory, this will install all required libraries

### Selecting Keyword
1. Run `python3 scrape.py` in the top-level directory
2. Enter the keyword of interest in the command line 
3. View the output of the program in `data/`once the program has finished (it will take some time)


