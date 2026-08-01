from config.setting import setting
from src.retrieval import retrieve_chunks
from src.gemini_client import generate_response
import google.generativeai as genai
from config.logger import logger


try:
    genai.configure(api_key=setting.gemini_api_key)
    model = genai.GenerativeModel(setting.gemini_model)
    logger.info("Gemini Model is Created")
except Exception as e:
    logger.info("Gemini Model Creation Failed %s",e)

def full_pipeline(query, history):
    try:
        context = retrieve_chunks(query)
        result = generate_response(model, query, context, history)
        logger.info("Successfully Generated Response")
        return result
    except Exception as e:
        logger.info("Failed To Generate the Response %s", e)
    

if __name__ == "__main__":

   
    full_pipeline(query, history)

