from html import escape

import resend
from model.schemas import emailform
from config.setting import setting
from config.logger import logger



def data_validation(name, email, question, message):
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    if not name.strip():
        raise ValueError("Name cannot be empty")
    if not isinstance(question, str):
        raise TypeError("Question must be a string")
    if not question.strip():
        raise ValueError("Question cannot be empty")
    if not isinstance(message, (str, type(None))):
        raise TypeError("Message must be a string or None")

    return emailform(
        name=name.strip(),
        email=email,
        question=question.strip(),
        message=message.strip() if message else None,
    )


    


def notifier(name,email,question,message):
    lead = data_validation(name, email, question, message)

    recipient_email = setting.client_email
    resend.api_key = setting.resend_api_key
   
    params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": [recipient_email],
    "subject": "New lead captured from your website chatbot",
    "html": f"""
    <p><strong>New lead from your website chatbot:</strong></p>
    <p>Name: {escape(lead.name)}<br>
    Email: {escape(str(lead.email))}<br>
    Question: {escape(lead.question)}<br>
    Additional message: {escape(lead.message) if lead.message else 'N/A'}</p>
    """,
    }
    try:
        response = resend.Emails.send(params)
        logger.info("Notification sent successfully")
        return response
    except Exception:
        logger.exception("Sending email failed")
        raise
