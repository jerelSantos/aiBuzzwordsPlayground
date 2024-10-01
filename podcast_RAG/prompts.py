
def get_podcast_prompt(retrieved_segments, pdf_scrape):
    podcast_prompt = [("system", """You will create a podcast script. You will be provided with examples of good conversational segments.
                        You should mimic their flow, tone, and engagement style, while applying the topic at hand.
                        Use the examples as a guide for structure and natural transitions."""
            ),
    ("human", f""" 
    Using the examples provided, generate a natural and engaging conversation between a host and a guest. The host should ask insightful questions, prompting the guest to share personal experiences and insights. Keep the flow dynamic and avoid too much technical exposition. 

    Here are the example conversational segements (delimited in <segments> XML tags). There are two speakers indicated by '(1)' and '(2)':
    <segments>{retrieved_segments}</segments>

    Now generate a podcast script based on the following topic:
    <pdf>{pdf_scrape}</pdf>
    """)]

    return podcast_prompt

def get_conversation_prompt(retrieved_segments, pdf_scrape):
    conversation_prompt = [("system", """You will create a transcript of a conversation between two people, person (2) who is an expert on a given topic and
                     person (1) who is interested in the topics person (2) is an expert in. Keep the conversation
                     between the two people relaxed and informal. It should sound like two friends just casually talking.
                     The conversation should NOT sound like a question and answer panel.
           
                     You will be provided with examples of good conversational segments.
                     You should mimic their flow, tone, and engagement style, while applying the topic at hand.
                     Use the examples as a guide for structure and natural transitions."""
           ),
("human", f""" 
Here are the examples of good conversational segements (delimited in <segments> XML tags). There are two speakers indicated by '(1)' and '(2)':
<segments>{retrieved_segments}</segments>

The topics discussed in the following pdf (delimited by <pdf> XML tags) are the topics that person (2) is an expert on:
<pdf>{pdf_scrape}</pdf>
""")]
    
    return conversation_prompt

def ssml_prompt(script):
    prompt = [("system", """You will be given a script of a conversation between two people (delimited by <conversation> XML tags). We are going to use Google Cloud Text-To-Speech to put voices behind this script. You are in charge of placing SSML tags in the conversation to achieve the following:
               1. Giving each speaker a distinctive voice.
               2. Giving life to the conversation by adding breaks, pauses, laughs, or emphasis on any words where you see fit.
               Feel free to use any SSML tags that are supported by Google Cloud Text-To-Speech."""
           ),
("human", f""" The following is a discussion between two people:
<conversation>{script}</conversation>

Please add SSML tags to it. So we can pass it into Google Clouds Text-To-Speech.
""")]
    
    return prompt