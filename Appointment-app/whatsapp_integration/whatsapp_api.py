import requests
import os

WHATSAPP_API_URL = "https://graph.facebook.com/v19.0/YOUR_PHONE_NUMBER_ID/messages"
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

def send_whatsapp_message(to_number: str, message: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    return response.status_code, response.json()
