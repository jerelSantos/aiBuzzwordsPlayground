import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from prompts import get_conversation_prompt, get_podcast_prompt, ssml_prompt

pdf_scrape = """I examine the incentives of professional mixed martial artists and how they influence the
strategies of the fighters in high profile competitions. Using data collected from hundreds of
professional fights, I examine the effects of 1st and 2nd round performance together on 3rd round
performance and on risky behavior, in bouts lasting three rounds. Using probability logistic regressions
to calculate performance, and linear regressions to estimate risk taking, we find that 1st and 2nd round
performance together have little effect on third round performance. However, a good (bad)
performance in the first 2 rounds reduces (increases) risk-taking behavior in the third round or changes
in risk-taking behavior in the 3rd round, relative to the first two rounds. We also examine the rare cases
of rematches, and find that while performance in the original fight is a good predictor of the outcome
and performance in a rematch, the actual outcome of the original fight is not. That is to say that fighters
who did well, but lost (by bad luck) in the original match are more likely to win the second match."""

load_dotenv()

# initialize openAI embeddings and Pinecone
pc_api_key = os.getenv('PINECONE_API_KEY')
oai_api_key = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key=oai_api_key, model='text-embedding-3-small')
pc = Pinecone(api_key=pc_api_key)

# get index of vectorDB from pinecone
index_name = 'podcast-rag'
index = pc.Index(index_name)

def retrieve_relevant_segments(pdf_topic):
    # embed pdf_topic as a vector
    embedded_pdf_topic = embeddings.embed_query(pdf_topic)

    # use embedded pdf_topic vector to get similar items from vectorDB
    results = index.query(
        vector=embedded_pdf_topic,
        top_k=10,
        include_metadata=True
    )

    # get vector values from results and return it
    segments = [match['metadata']['text'] for match in results['matches']]

    return segments

# use retrieve_relevant_segments() function to do exactly that
retrieved_segments = retrieve_relevant_segments(pdf_scrape)
retrieved_segments = "\n\n".join(retrieved_segments)

# generate prompt using retrieved_segments and pdf_scrape
prompt = get_conversation_prompt(retrieved_segments, pdf_scrape)

# setup chatgpt 4o and use prompt to generate podcast script
llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0
)
print("Prompting OpenAI for script...")
response = llm.invoke(prompt)
print("Done!")

text_file = open("basic_rag_output.txt", "w")
text_file.write(response.content)
text_file.close()

# use OpenAI to add SSML tags to the conversation
prompt = ssml_prompt(response.content)
print("Prompting OpenAI to add SSML tags...")
response = llm.invoke(prompt)
print("Done!")

text_file = open("ssml_tags.txt", "w")
text_file.write(response.content)
text_file.close()