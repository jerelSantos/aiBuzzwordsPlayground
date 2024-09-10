import os
import requests
from pinecone import Pinecone
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver

url = "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-162-with-belal-muhammad"

# initialize pinecone with API key from env file
load_dotenv()
pc_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pc_api_key)

# create index for podcast transcripts in pinecone
# index_name = "podcast-transcripts"
# if not pc.has_index(index_name):
#     pc.create_index(
#         name = index_name,
#         dimension = 1536
#     )

# initialize BeautifulSoup to scrape website for transcript
response = requests.get(url)
#print(response.content)
soup = BeautifulSoup(response.content, "html.parser")

# scrape website for transcript
transcript = soup.find_all("div", {"class": "hsp-episode-body"})

for x in transcript:
    print(x)