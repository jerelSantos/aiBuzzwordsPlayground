
def llm1_outline_prompt(pdf_scrape):
    outline = [("system", (
        f"""You will be given the text from a pdf file (delimited by <pdf> XML tags). """
        f"""Your job is to read through the text and create an outline for a podcast episode about the topics discussed in the pdf. """
        f"""The outline should include 3-5 key topics that flow naturally into one another, with a focus on maintaining audience engagement."""
    )),
    ("human", (
        f"""The following is text extracted from a pdf file (delimited by <pdf> XML tags). """
        f"""Please generate an outline for a podcast episode based on the topics from the pdf. """
        f"""<pdf>{pdf_scrape}</pdf>"""
    ))]

    return outline

# conversation method
prompt2 = ("Based on the following outline of topics:" 
            "\n--------------OUTLINE--------------\n{outline}\n--------------END OUTLINE--------------\n"
            "You will create a transcript of a conversation between two people, person (2) who is an expert on a given topic and "
            "person (1) who is interested in the topics person (2) is an expert in. Keep the conversation "
            "between the two people relaxed and informal. It should sound like two friends just casually talking. "
            "The conversation should NOT sound like a question and answer panel.")

# podcast method
prompt2 = ("Using the following outline:" 
            "\n--------------OUTLINE--------------\n{outline}\n--------------END OUTLINE--------------\n"
            "Please generate a conversational podcast script where a host and a guest discuss each topic. " 
            "Transitions between each topic should be seamless. The host should ask engaging, open-ended questions, " 
            "and the guest should provide detailed yet conversational responses. Keep the tone light and accessible."
            "Be sure to only include the script in your response, since I am directly importing your response into another LLM to revise.")