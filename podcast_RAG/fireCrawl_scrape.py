import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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

    print("scraped url: {}".format(scrape_status['metadata']['title']))

    # use BeautifulSoup to get dialogue from html
    soup = BeautifulSoup(scrape_status['html'], 'html.parser')
    hsp_paragraphs = soup.find_all('div', class_='hsp-paragraph')

    # store each dialogue text as an element in dialogue[]
    dialogue = []
    for i, div in enumerate(hsp_paragraphs):
        paragraph = div.find('p')

        # insert (1) or (2) depending on speaker
        if i % 2 == 0:
            line = "(1): " + paragraph.get_text()
        else:
            line = "(2): " + paragraph.get_text()
        
        dialogue.append(line)

    print("Dialogue successfully scraped: {}".format(dialogue[0]))
    return dialogue