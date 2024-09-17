# 🤔 What is this repo?
I'm a total newbie when it comes to this AI/LLM optimization stuff for my web apps. So this repo is for me to test and mess around with any solution approaches before implementing them into my actual web apps. <br /><br />

Each header in this README will detail a problem and the solution approaches will follow. <br />
Documentation for each solution will include:
<ul>
    <li>A general text summary of the solution</li>
    <li>A workflow graph of the solution (if i'm not too lazy to make one)</li>
    <li>Each step of the solution in further detail</li>
    <li>Result metrics (cost, effectiveness, etc.)</li>
</ul>

# 🤬 Pods Issue 1: Our Podcast Scripts SUCK and are EXPENSIVE 
Pods is my project where user's input any pdf file (like a textbook) and our app will output a podcast based on the topics discussed in the pdf file. <br />
We currently use OpenAI's gpt-4o-2024-08-06 model to create our podcast scripts. Here's the context we give it:
```
You create scripts for podcasts. You can understand the flow of human conversation. The podcast has two personalities: the host and the guest. The goal of the podcast is for it to not only be entertaining but also informative of the given topic, allowing the listener to get a better understanding of the guest's personality, interests, and topic they're an expert on.
```
And the following is the prompt the model is given:
```typescript
`Create a podcast script about the topic from the given pdf (delimited in XML tags):
    <pdf>${pdf}<pdf>`
```
Obviously my prompt engineering leaves much to be desired, but even with high level prompt engineering, this (probably) won't solve the issue of price. So let's get into some solutions!

# 🤓 Solution 1: RAG
[podcast_RAG directory](/podcast_RAG/)
## Solution Summary:
Retrieval-Augmented Generation (RAG) is the idea of providing additional context in the prompt when communicating with a model. For our usecase, we will provide OpenAI's ChatGPT model with segments of real podcasts so it will learn what good conversation is in order to apply it to the podcast script it gives us. <br/> <br/>
The general workflow will look like this:
<ol>
    <li>Scrape internet for podcast transcripts using FireCrawl</li>
    <li>Store random segments of the podcast transcripts in a vector DB using Pinecone</li>
    <li>When generating podcast script, get relevant info from vector DB and place it in prompt</li>
</ol>
Pretty simple, yeah?<br/>
Well maybe for most competent developers. But that's not me. So let's go into further detail of each step!

### Step 1: Scrape internet for podcast transcripts
[fireCrawl_scrape.py](/podcast_RAG/fireCrawl_scrape.py)<br/><br/>
As of right now, all this file does it takes in a URL from happyscribe and takes the podcast script here, and puts each line of the transcript as it's own item in a 'dialogue' array, and returns this. <br/><br/>
In the future, I'd like this to be automated with the help of LLMs.

### Step 2: Store segments of podcasts in a vector DB
[vectorDBstore.py](/podcast_RAG/vectorDBstore.py)<br/><br/>
As of right now, we choose 100 random segments from the podcast transcript of length 6, 8, or 10 lines and store this in the Pinecone vector DB.
We store the raw text of the segments as metadata. <br>


### Step 3: Use vector DB when generating podcast script
[RAG_script.py](/podcast_RAG/RAG_script.py)<br/><br/>
Once we have our vectors and text stored in our Pinecone vectorDB, we can grab relevant segments and insert them into our prompt. <br/><br/>

Here's the system context we give it:
```
You will create a podcast script. You will be provided with examples of good conversational segments.

You should mimic their flow, tone, and engagement style, while applying the topic at hand.
Use the examples as a guide for structure and natural transitions.
```

Here's the prompt:
```python
f""" 
Using the examples provided, generate a natural and engaging conversation between a host and a guest. The host should ask insightful questions, prompting the guest to share personal experiences and insights. Keep the flow dynamic and avoid too much technical exposition.

Here are the example conversational segements (delimited in <segments> XML tags). There are two speakers indicated by '(1)' and '(2)':
<segments>{retrieved_segments}</segments>

Now generate a podcast script based on the following topic:
<pdf>{pdf_scrape}</pdf>
"""
```

## 🔬 And the result is:
[basic_rag_output.txt](podcast_RAG/outputs/basic_rag_output.txt)<br>
Here's the output of solution 1:
```
**Podcast Script: The Fight Game: Strategy, Performance, and Risk in MMA**

**[INTRO MUSIC FADES IN]**

**(1) Host:** Welcome back to "The Fight Game," where we dive deep into the world of mixed martial arts, exploring the strategies, performances, and the psychology behind the fighters. I’m your host, Alex, and today we have a fascinating topic on our hands. We’re going to examine the incentives of professional mixed martial artists and how these incentives influence their strategies in high-profile competitions. Joining me today is Dr. Jamie Carter, a sports analyst who has spent years studying fight performance data. Jamie, welcome to the show!

**(2) Guest:** Thanks for having me, Alex! I’m excited to be here and talk about this intriguing aspect of MMA.

**(1) Host:** So, let’s jump right in. You’ve analyzed data from hundreds of professional fights. What were some of the key findings regarding how fighters perform in the first two rounds and how that affects their performance in the third round?

**(2) Guest:** Great question! What we found is that the performance in the first two rounds doesn’t significantly impact how a fighter performs in the third round. It’s almost like they reset mentally. However, there’s a twist—if a fighter has a good performance in the first two rounds, they tend to take fewer risks in the third round. Conversely, if they struggle early on, they might become more reckless as they try to salvage the fight.

**(1) Host:** That’s really interesting! So, it’s almost like a psychological game at play. If they feel confident, they play it safe, but if they’re behind, they go for broke. Have you seen this reflected in any specific fights?

**(2) Guest:** Absolutely! Take a look at the fight between Max Holloway and Brian Ortega. In the early rounds, Holloway was dominating, and you could see Ortega becoming more cautious as the fight progressed. He was trying to find openings but was also aware that he couldn’t afford to get reckless. It’s a delicate balance.

**(1) Host:** Right, and that makes sense. It’s like a chess match where each move influences the next. Now, you also looked into rematches. What did you discover about fighters who performed well but lost in their first encounter?

**(2) Guest:** That’s a fascinating aspect! We found that fighters who performed well in the original fight, even if they lost due to bad luck or a controversial decision, were more likely to win in a rematch. It’s almost as if the confidence from their previous performance carries over, despite the outcome.

**(1) Host:** So, it’s not just about the win or loss, but how they feel about their performance? That’s a huge insight! 

**(2) Guest:** Exactly! It’s all about the mindset. If a fighter believes they can replicate their success, they’re more likely to adjust their strategy effectively in the rematch.

**(1) Host:** That’s a game-changer for how we view these fighters and their journeys. Now, let’s talk about risk-taking behavior. You mentioned that a bad performance in the first two rounds can lead to increased risk-taking in the third. Can you elaborate on that?

**(2) Guest:** Sure! When fighters feel they’re behind, they often resort to high-risk maneuvers, hoping for a quick finish. This can lead to exciting moments in fights, but it can also backfire. For instance, if a fighter knows they need a knockout to win, they might throw caution to the wind and leave themselves open to counterattacks.

**(1) Host:** It’s like a double-edged sword. They’re trying to create an opportunity, but it could also lead to their downfall. Have you seen any memorable examples of this in recent fights?

**(2) Guest:** Definitely! Look at the fight between Tony Ferguson and Justin Gaethje. Ferguson was behind on the scorecards and started taking wild risks, which ultimately led to his defeat. It was a classic case of a fighter trying to turn the tide but getting caught in the process.

**(1) Host:** Wow, that’s a perfect illustration of the concept. It really highlights the mental aspect of fighting. So, as we wrap up, what do you think this means for fighters and their training strategies moving forward?

**(2) Guest:** I think it emphasizes the importance of mental preparation just as much as physical training. Fighters need to develop strategies not just for their opponents but also for managing their own psychology during the fight. Understanding how to handle pressure and risk can be the difference between winning and losing.

**(1) Host:** That’s a powerful takeaway. Jamie, thank you so much for sharing your insights with us today. It’s been a pleasure having you on the show!

**(2) Guest:** Thanks for having me, Alex! I enjoyed our conversation.

**(1) Host:** And to our listeners, thank you for tuning in to "The Fight Game." Don’t forget to subscribe and join us next week as we continue to explore the fascinating world of mixed martial arts. Until then, keep fighting the good fight!

**[OUTRO MUSIC FADES OUT]**
```
## Closing thoughts
Yeah the result is still buns. It seems that instead of taking the 

# 🤓 Solution 2: There is no Podcast
[podcast_RAG/prompts.py](podcast_RAG/prompts.py)
## Solution Summary:
This one isn't that complicated. We just adjust the prompt to produce a (hopefully) better solution. <br/><br/>

The big problem here is that the podcast script still sounds like the guest info dumping onto the host. Maybe we can completely throw out any mentions of "podcast" from the prompt and prompt the model to make just a conversation between two friends. This way, the conversation will sound more natural? <br/><br/>

Here's the new system context:
```
You will create a transcript of a conversation between two people, person (2) who is an expert on a given topic and
person (1) who is interested in the topics person (2) is an expert in. Keep the conversation between the two people relaxed and informal. It should sound like two friends just casually talking. The conversation should NOT sound like a question and answer panel.
           
You will be provided with examples of good conversational segments. You should mimic their flow, tone, and engagement style, while applying the topic at hand. Use the examples as a guide for structure and natural transitions.
```

And here's the new prompt:
```python
f"""
Here are the examples of good conversational segements (delimited in <segments> XML tags). There are two speakers indicated by '(1)' and '(2)':
<segments>{retrieved_segments}</segments>

The topics discussed in the following pdf (delimited by <pdf> XML tags) are the topics that person (2) is an expert on:
<pdf>{pdf_scrape}</pdf>
"""
```
## 🔬 And the result is:
[conversation_output_RAG.txt](podcast_RAG/outputs/conversation_output_RAG.txt)<br/><br/>
Here's the output with the new prompt (and RAG):
```
(1): So, I’ve been thinking about how fighters approach their strategy in a match. Like, do you think their performance in the first couple of rounds really sets the tone for the rest of the fight?

(2): Oh, absolutely! It’s fascinating how that works. I’ve looked into it a bit, and it turns out that the performance in the first two rounds doesn’t really dictate how they’ll do in the third round. It’s more about how they react to their earlier performance.

(1): Really? So, if they do well in the first two rounds, it doesn’t guarantee they’ll keep that momentum going?

(2): Exactly! If they have a good first round, they might actually play it safe in the third. It’s like they’re thinking, “I’ve got a lead, let’s not mess this up.” On the flip side, if they’re behind, they might take more risks to try and turn things around.

(1): That makes sense. It’s like a psychological game as much as a physical one. So, what about rematches? Do fighters change their strategies based on what happened the first time?

(2): Oh, for sure! Interestingly, the performance in the original fight is a good predictor of how they’ll do in the rematch, but the actual outcome doesn’t always follow. Like, if a fighter performed well but lost due to bad luck, they’re often more likely to win the rematch.

(1): That’s wild! So, it’s almost like they learn from their mistakes, but the outcome of the first fight doesn’t really matter as much as how they fought?

(2): Exactly! It’s all about adapting and learning. Fighters can take those lessons and adjust their strategies for the rematch. It’s a whole different ball game.

(1): I love that! It’s like a chess match, but with punches. So, do you think this affects how fans view the fighters? Like, do they get too caught up in the win-loss record?

(2): Definitely! Fans often focus on the outcomes rather than the nuances of the performance. They might not realize that a fighter could have had a stellar performance but just got caught at the wrong moment. It’s all about the context.

(1): Right! It’s like, “Hey, that was a great fight, even if they lost!” I guess it’s all part of the drama that makes MMA so exciting.

(2): Exactly! The unpredictability is what keeps everyone on the edge of their seats. You never know how a fighter will adapt or what they’ll bring to the rematch. It’s all part of the sport’s charm.
```

## Closing Thoughts
I think both the podcast and conversational method have their own choices. I think in the future, I'll allow the user to dictate what tone they want, and from there I'll place the keywords they choose into the prompt strategically.