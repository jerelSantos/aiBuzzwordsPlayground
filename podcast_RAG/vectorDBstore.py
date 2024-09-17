import os
import time
from dotenv import load_dotenv
from fireCrawl_scrape import getDialogue
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec
from random import randrange, choice
from uuid import uuid4

urls = [ "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-155-with-max-holloway",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/2195-andrew-huberman",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-162-with-belal-muhammad",
        "https://www.happyscribe.com/public/the-diary-of-a-ceo-with-steven-bartlett/andrew-huberman-you-must-control-your-dopamine-the-shocking-truth-about-cold-showers",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/2187-adam-sandler",
        "https://www.happyscribe.com/public/lex-fridman-podcast-artificial-intelligence-ai/139-andrew-huberman-neuroscience-of-optimal-performance",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/1527-david-blaine",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/1532-mike-tyson",
        "https://www.happyscribe.com/public/the-diary-of-a-ceo-with-steven-bartlett/the-muscle-building-expert-creatine-loading-is-a-waste-of-time-they-re-lying-to-you-about-workout-hours-dr-michael-israetel"
]

load_dotenv()

# iterate over all urls to get 25 dialogue segments from each url
dialogue_segments = []
for url in urls:
        print("scraping url: {} ...".format(url))
        # get dialogue from transcript from given url
        dialogue = getDialogue(url)

        # get 100 random segments of the dialogue, ranging from length 2, 4, or 6
        for i in range(100):
                start = randrange(len(dialogue[:-6]))
                end = choice([6, 8, 10])
                dialogue_segments.append(" ".join(dialogue[start:start + end]))

print("dialogue successfully segmented: {}".format(dialogue_segments[0]))

# setup pinecone
pc_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pc_api_key)

# initialize vectorDB segment in pinecone if not already existing
index_name = 'podcast-rag'
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    print("Index {} does not exist. Creating new index...".format(index_name))
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)
index = pc.Index(index_name)

# setup openAI embeddings
oai_api_key = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key=oai_api_key, model='text-embedding-3-small')

# use vectorStores from langchain to store dialogue segments in vectorstore
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

documents = []
for segment in dialogue_segments:
      new_doc = Document(page_content=segment, metadata={"text": segment})
      documents.append(new_doc)

uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)