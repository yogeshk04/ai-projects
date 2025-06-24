from openai import OpenAI

def detect_intent(messages):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    content = response.choices[0].message.content
    return extract_intent_from_text(content)

def extract_intent_from_text(text):
    if "book" in text.lower() and "appointment" in text.lower():
        return "book_appointment"
    return "unknown"
