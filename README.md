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
```python
"You create scripts for podcasts. You can understand the flow of human conversation. The podcast has two personalities: the host and the guest. The goal of the podcast is for it to not only be entertaining but also informative of the given topic, allowing the listener to get a better understanding of the guest's personality, interests, and topic they're an expert on."
```
And the following is the prompt the model is given:
```python
"Create a podcast script about the topic from the given pdf (delimited in XML tags):
    <pdf>${pdf}<pdf>"
```
Obviously my prompt engineering leaves much to be desired, but even with high level prompt engineering, this (probably) won't solve the issue of price. So let's get into some solutions!

## 🤓 Solution 1: RAG
[All Files Here](/podcast_RAG/)
### Solution Summary:
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
[Relevant File](/podcast_RAG/fireCrawl_scrape.py)<br/><br/>
As of right now, all this file does it takes in a URL from happyscribe and takes the podcast script here, and puts each line of the transcript as it's own item in a 'dialogue' array, and returns this. <br/><br/>
In the future, I'd like this to be automated with the help of LLMs.

### Step 2: Store segments of podcasts in a vector DB
[Relevant File](/podcast_RAG/vectorDBstore.py)<br/><br/>
As of right now, we choose 25 random segments from the podcast transcript of length 2, 4, or 6 lines and store this in the Pinecone vector DB. <br/><br/>
Right now the lines are labelled with (1) and (2). In the future, I'd like to test if replacing (1) and (2) with 'Host' and 'Guest' will have any impact on the output. <br> 

### Step 3: Use vector DB when generating podcast script