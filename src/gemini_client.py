from config.setting import setting
from src.retrieval import retrieve_chunks
from config.logger import logger


def generate_response(model, query, context, history):
    prompt = f"""
    You are a knowledgeable assistant for an Dental Clinic. Answer questions directly and confidently.

    ## Voice and Tone ##
    Respond in a formal, professional tone.

    ## RULES ##
    - Only Provide answer within Context.
    - If you don't have enough information to answer, use the fallback message. and Do not use outside knowledge as well as assumptions.
    - Keep responses concise and to the point
    - Respond in plain text only. No markdown, no bullet points, no asterisks, no bold formatting.
    - Make sure to keep the answer concise and to the point based on what's asked.
    - Never say "details are available", "information is available", "records show", "not detailed in the provided information" or any phrase implying you are referencing a document or database. Speak as if you know this information directly.. Answer directly and confidently as a knowledgeable assistant.
    
    
    ## Uncertainity Rules ##
    - Only fallback if context has absolutely no relevant information to the query. If context is partial, answer with what's available and note that more details can be obtained from the team.
    - When your answer is partial or incomplete, always end with exactly this phrase word for word: "For further details on assistance, please contact the team [[LEAD_FORM]] ", Do not explain the marker or mention it to the user.
    ## Context ##
    {context}

    ## History ##
    {history}
    ## Query ##
    {query}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        logger.info("Response Generated Successfully!")
        return text
    except Exception as e:
        logger.info("Response Generation Failed! %s",e)

    
    


if __name__ == "__main__":
    context = retrieve_chunks(query)
    generate_response(model, query, context, history)






