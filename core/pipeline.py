from config.setting import setting
from core.retrieval import retrieve_chunks
from core.gemini_client import generate_response
import google.generativeai as genai
from config.logger import logger
from model.schemas import intent_detection, Category


try:
    genai.configure(api_key=setting.gemini_api_key)
    model = genai.GenerativeModel(setting.gemini_model)
    logger.info("Gemini Model is Created")
except Exception as e:
    logger.info("Gemini Model Creation Failed %s",e)

def full_pipeline(query, history):
    try:
        context = retrieve_chunks(query)
        results = generate_response(model, query, context, history)
        answer_text  = results.answer
        show_form = "[[LEAD_FORM]]" in answer_text or results.category == Category.genuine_lead
        logger.info("Successfully Generated Response")
        return answer_text, show_form
    except Exception as e:
        logger.info("Failed To Generate the Response %s", e)
        return None, False
    

if __name__ == "__main__":

   
    full_pipeline(query, history)

