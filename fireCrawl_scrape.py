import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup

url = "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-162-with-belal-muhammad"

def getDialogue(url):
    # initialize firecrawl with API key from env file
    load_dotenv()
    fc_api_key = os.getenv('FIRECRAWL_API_KEY')
    fc = FirecrawlApp(api_key=fc_api_key)

    # scrape website via url using firecrawl
    scrape_status = fc.scrape_url(
    url, 
    params={'formats': ['markdown', 'html']}
    )

    # use BeautifulSoup to get dialogue from html
    soup = BeautifulSoup(scrape_status['html'], 'html.parser')
    hsp_paragraphs = soup.find_all('div', class_='hsp-paragraph')

    # store each dialogue text as an element in dialogue[]
    dialogue = []
    for div in hsp_paragraphs:
        paragraph = div.find('p')
        dialogue.append(paragraph.get_text())

    return dialogue