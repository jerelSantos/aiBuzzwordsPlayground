# https://langchain-ai.github.io/langgraph/concepts/low_level/

import os
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings, ChatOpenAI, OpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from prompts import llm1_outline_prompt

with open('bodybuilding.txt', 'r', encoding="utf8") as file:
    pdf_scrape = file.read()
    file.close()

# initialize API keys
load_dotenv()
oai_api_key = os.getenv('OPENAI_API_KEY')
pc_api_key = os.getenv('PINECONE_API_KEY')
lc_api_key = os.getenv('LANGCHAIN_API_KEY')
ggl_api_key = os.getenv('GOOGLE_API_KEY')

# initialize openai embeddings
embeddings = OpenAIEmbeddings(openai_api_key=oai_api_key, model='text-embedding-3-small')

# initialize pinecone
pc = Pinecone(api_key=pc_api_key)
index_name = 'podcast-chain'
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# node 1 - LLM_1: generate outline of podcast script
llm = ChatOpenAI(api_key=oai_api_key, model="gpt-4o-mini-2024-07-18")
prompt1 = PromptTemplate.from_template("The following is text extracted from a pdf file (delimited by <pdf> XML tags). Please generate an outline for a podcast episode based on the topics from the pdf. The outline should include 3-5 key topics that flow naturally into one another, with a focus on maintaining audience engagement. <pdf>{pdf}</pdf>")

chain1 = prompt1 | llm | StrOutputParser()

# print(chain1.invoke({"pdf": pdf_scrape}))

# node 2 - LLM_2: fill in dialogue segments of podcast script
prompt2 = PromptTemplate.from_template("The following is an outline for a podcast script. Please fill in dialogue relevant to the topics in the outline between two personalities: the host and guest. <outline{outline}</outline>")

chain2 = prompt2 | llm | StrOutputParser()

final_chain = chain1 | chain2
print(final_chain.invoke({"pdf": pdf_scrape}))