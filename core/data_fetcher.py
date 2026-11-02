import asyncio
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai
from config.setting import setting
from pathlib import Path


genai.configure(api_key=setting.gemini_api_key)
model = genai.GenerativeModel(setting.gemini_model)


async def main():
    async with AsyncWebCrawler() as crawler:
        content = await crawler.arun("")
        result = content.markdown
    
    return result

def clean_content(result):
    prompt = f"""
    Act as an expert content extraction. You have to extract this website content as it is
    Your task is to extract only content mention in this website ignoring all other things.
    
    #RULES
    - Make sure to extract content heading wise
    - Do not add something that is not in content

    HARD FILTERING
    - Ignore ALL of the following:
    - HTML tags
    - CSS
    - JavaScript
    - Navigation menus
    - Headers/footers
    - Repeated UI elements

    CLEAN OUTPUT
    - Output MUST be plain text only
    - No HTML tags
    - Preserve original wording exactly
    - Preserve punctuation and formatting

    OUTPUT FORMAT
    - Each section starts with its heading
    - Then its full extracted content
    - No explanations
    - No extra text

    CRITICAL:
    - Do NOT return the full page
    - Do NOT include raw HTML
    - Do NOT guess sections
    - Only return clean extracted sections

    # Here content
    {result}

    """

    response = model.generate_content(prompt)
    text = response.text
    clean_text = text.replace("*","").replace("-"," ")

    with open("data/.txt", 'w', encoding="utf-8") as f:
        f.write(clean_text)






if __name__ == "__main__":
    result = asyncio.run(main())
    clean_content(result)