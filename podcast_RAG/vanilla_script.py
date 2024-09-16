import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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
oai_api_key = os.getenv('OPENAI_API_KEY')

prompt = [("system", "You create scripts for podcasts. You can understand the flow of human conversation. The podcast has two personalities: the host and the guest. The goal of the podcast is for it to not only be entertaining but also informative of the given topic, allowing the listener to get a better understanding of the guest's personality, interests, and topic they're an expert on."),
("human", f""" 
Create a podcast script about the topic from the given pdf (delimited in XML tags):
<pdf>{pdf_scrape}</pdf>
""")]

llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    temperature=0
)
print("Prompting OpenAI...")
response = llm.invoke(prompt)

print(response)

text_file = open("vanilla_podcast_output.txt", "w")
text_file.write(response.content)
text_file.close()