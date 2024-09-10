import os
from firecrawl import FirecrawlApp
from pinecone import Pinecone
from dotenv import load_dotenv
from bs4 import BeautifulSoup

url = "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-162-with-belal-muhammad"

# initialize pinecone and firecrawl with API key from env file
load_dotenv()
pc_api_key = os.getenv('PINECONE_API_KEY')
fc_api_key = os.getenv('FIRECRAWL_API_KEY')
pc = Pinecone(api_key=pc_api_key)
fc = FirecrawlApp(api_key=fc_api_key)

# create index for podcast transcripts in pinecone
# index_name = "podcast-transcripts"
# if not pc.has_index(index_name):
#     pc.create_index(
#         name = index_name,
#         dimension = 1536
#     )

# scrape website via url using firecrawl
scrape_status = fc.scrape_url(
  url, 
  params={'formats': ['markdown', 'html']}
)

soup = BeautifulSoup(scrape_status['html'], 'html.parser')

hsp_paragraphs = soup.find_all('div', class_='hsp-paragraph')
dialogue = []
for i, div in enumerate(hsp_paragraphs):
    paragraph = div.find('p')
    dialogue.append(paragraph.get_text())

for d in dialogue:
    print(d)

# with open("htmlOutput.txt", "w") as text_file:
#     text_file.write(scrape_status['html'])