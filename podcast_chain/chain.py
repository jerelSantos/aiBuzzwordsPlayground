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

# initialize openai from langchain_openai
embeddings = OpenAIEmbeddings(openai_api_key=oai_api_key, model='text-embedding-3-small') 
llm = ChatOpenAI(api_key=oai_api_key, model="gpt-4o-mini-2024-07-18")

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
prompt1 = PromptTemplate.from_template("The following is text extracted from a pdf file. "
                                       "Please generate an outline for a podcast episode based on the topics from the pdf. "
                                       "The outline should include 3-5 key topics that flow naturally into one another, " 
                                       "with a focus on maintaining audience engagement. "
                                       "\n--------------PDF--------------\n{pdf}\n--------------END PDF--------------"
                                       "Be sure to only include the outline in your response, since I am directly importing your response into another LLM to revise.")
chain1 = prompt1 | llm | StrOutputParser() # basic chain for node 1: prompt -> llm -> string output

# node 2 - LLM_2: fill in dialogue segments of podcast outline
prompt2 = PromptTemplate.from_template("Based on the following outline of topics:" 
                                       "\n--------------OUTLINE--------------\n{outline}\n--------------END OUTLINE--------------\n"
                                       "You will create a transcript of a conversation between two people, person (2) who is an expert on a given topic and "
                                       "person (1) who is interested in the topics person (2) is an expert in. Keep the conversation "
                                       "between the two people relaxed and informal. It should sound like two friends just casually talking. "
                                       "The conversation should NOT sound like a question and answer panel.")
chain2 = prompt2 | llm | StrOutputParser() # basic chain for node 2: output of node1 -> llm -> string output

# node 3 - LLM_3: enhance transitions of the podcast script
# prompt3 = PromptTemplate.from_template("Given the following script for a podcast: \n--------------SCRIPT--------------\n{script}\n--------------END SCRIPT--------------\n Please enhance the transitions between each topic. Ensure each transition feels natural and engaging, avoiding repetitive phrases like 'moving on' or 'next.' Use conversational cues that keep the audience engaged.")
# chain3 = prompt3 | llm | StrOutputParser()

# node 4 - LLM_4: enhance the overall tone of the podcast script
prompt3 = PromptTemplate.from_template("Review the following script for a podcast: "
                                       "\n--------------SCRIPT--------------\n{script}\n--------------END SCRIPT--------------\n " 
                                       "Please polish the tone to make it more engaging. Add occasional humor, rhetorical questions, " 
                                       "or personal anecdotes where appropriate to make the conversation feel more human and lively."
                                       "Be sure to only include the script in your response, since I am directly importing your response into another LLM to revise.")
chain3 = prompt3 | llm | StrOutputParser() # basic chain for node 3: output of node2 -> llm -> string output

# get example pdf 'bodybuilding.txt' (hardcoded):
with open('bodybuilding.txt', 'r', encoding="utf8") as file:
    pdf_scrape = file.read()
    file.close()

# assemble and call final LLM chain
final_chain = chain1 | chain2 | chain3 # final chain goes: node1 -> node2 -> node3
final_chain.invoke({"pdf": pdf_scrape}) # run the chain (output is on langsmith)