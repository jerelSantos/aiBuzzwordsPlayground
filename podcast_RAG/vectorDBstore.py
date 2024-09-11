from podcast_RAG.fireCrawl_scrape import getDialogue
from random import randrange, choice

urls = [ "https://www.happyscribe.com/public/the-joe-rogan-experience/2195-andrew-huberman",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-155-with-max-holloway",
        "https://www.happyscribe.com/public/the-joe-rogan-experience/jre-mma-show-162-with-belal-muhammad"
]
url = urls[2]

# get dialogue from transcript from given url
dialogue = getDialogue(url)

# get 25 random segments of the dialogue, ranging from length 2, 4, or 6
dialogue_segments = []
for i in range(25):
    start = randrange(len(dialogue[:-6]))
    end = choice([2, 4, 6])
    dialogue_segments.append(dialogue[start:start + end])

