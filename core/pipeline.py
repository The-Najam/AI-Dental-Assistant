from config.setting import setting
from core.retrieval import retrieve_chunks
from core.generation import generate_response
import google.generativeai as genai
from config.logger import logger
from model.schemas import Chat_Response, Category


try:
    genai.configure(api_key=setting.gemini_api_key)
    model = genai.GenerativeModel(setting.gemini_model)
    logger.info("Gemini Model is Created")
except Exception as e:
    logger.exception("Gemini Model Creation Failed %s",e)
    raise

def full_pipeline(query, history):
    try:
        context = retrieve_chunks(query)
        results = generate_response(model, query, context, history)
        if not isinstance(results,Chat_Response):
            raise TypeError("Response is Not object")
        if not results:
            raise ValueError("Response is Empty")
        answer_text  = results.answer
        show_form = "[[LEAD_FORM]]" in answer_text or results.category == Category.genuine_lead
        logger.info("Successfully Generated Response")
        return answer_text, show_form
    except Exception as e:
        logger.exception("Failed To Generate the Response %s", e)
        raise
    

if __name__ == "__main__":
    query = "tell me how to get rid of crowns?"
    history = ""

    response,show_form = full_pipeline(query, history)
    print(response)
    print(show_form)

