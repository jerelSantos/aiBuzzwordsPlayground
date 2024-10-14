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

# initialize API keys
load_dotenv()
oai_api_key = os.getenv('OPENAI_API_KEY')
pc_api_key = os.getenv('PINECONE_API_KEY')
lc_api_key = os.getenv('LANGCHAIN_API_KEY')
ggl_api_key = os.getenv('GOOGLE_API_KEY')

# initialize openai embeddings
embeddings = OpenAIEmbeddings(openai_api_key=oai_api_key, model='text-embedding-3-small')

# initialize pinecone
# pc = Pinecone(api_key=pc_api_key)
# index_name = 'podcast-chain'
# existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
# if index_name not in existing_indexes:
#     pc.create_index(
#         name=index_name,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1"),
#     )
# index = pc.Index(index_name)
# vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# node 1 - LLM_1: generate outline of podcast script
llm = ChatOpenAI(api_key=oai_api_key, model="gpt-4o-mini-2024-07-18")
prompt1 = PromptTemplate.from_template("The following is text extracted from a pdf file (delimited by <pdf> XML tags). Please generate an outline for a podcast episode based on the topics from the pdf. The outline should include 3-5 key topics that flow naturally into one another, with a focus on maintaining audience engagement. \n--------------PDF--------------\n{pdf}\n--------------END PDF--------------")
chain1 = prompt1 | llm | StrOutputParser()

# node 2 - LLM_2: fill in dialogue segments of podcast outline
prompt2 = PromptTemplate.from_template("Using the following outline: \n--------------OUTLINE--------------\n{outline}\n--------------END OUTLINE--------------\n Please generate a conversational podcast script where a host and a guest discuss each topic. The host should ask engaging, open-ended questions, and the guest should provide detailed yet conversational responses. Keep the tone light and accessible.")
chain2 = prompt2 | llm | StrOutputParser()

# node 3 - LLM_3: enhance transitions of the podcast script
prompt3 = PromptTemplate.from_template("Given the following script for a podcast: \n--------------SCRIPT--------------\n{script}\n--------------END SCRIPT--------------\n Please enhance the transitions between each topic. Ensure each transition feels natural and engaging, avoiding repetitive phrases like 'moving on' or 'next.' Use conversational cues that keep the audience engaged.")
chain3 = prompt3 | llm | StrOutputParser()

# node 4 - LLM_4: enhance the overall tone of the podcast script
prompt4 = PromptTemplate.from_template("Review the following script for a: \n--------------SCRIPT--------------\n{script}\n--------------END SCRIPT--------------\n Please polish the tone to make it more engaging. Add occasional humor, rhetorical questions, or personal anecdotes where appropriate to make the conversation feel more human and lively.")
chain4 = prompt4 | llm | StrOutputParser()

# get example pdf 'bodybuilding.txt' (hardcoded):
with open('bodybuilding.txt', 'r', encoding="utf8") as file:
    pdf_scrape = file.read()
    file.close()

# assemble and call final LLM chain
final_chain = chain1 | chain2 | chain3 | chain4
print(final_chain.invoke({"pdf": pdf_scrape}))