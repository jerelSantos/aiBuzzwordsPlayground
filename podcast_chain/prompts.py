
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

