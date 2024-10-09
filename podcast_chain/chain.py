# https://langchain-ai.github.io/langgraph/concepts/low_level/

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from prompts import llm1_outline_prompt

load_dotenv()
oai_api_key = os.getenv('OPENAI_API_KEY')

# setup anything that needs an api key
llm = ChatOpenAI(
    openai_api_key=oai_api_key,
    model="gpt-4o-mini-2024-07-18",
    temperature=0
)

# define nodes
# node 1: given pdf, LLM-1 will generate script outline
def generate_outline(pdf):
    prompt = llm1_outline_prompt()

    return prompt

