from ai_chatbot.workflow.chatbot_workflow import app, ChatState
from ai_chatbot.whatsapp_integration.whatsapp_api import send_whatsapp_message

def handle_whatsapp_message(from_number: str, user_message: str):
    initial_state = ChatState(messages=[{"role": "user", "content": user_message}])
    final_state = app.invoke(initial_state)

    for msg in final_state.messages:
        if msg["role"] == "assistant":
            send_whatsapp_message(from_number, msg["content"])

# Example usage (simulate incoming message)
if __name__ == "__main__":
    handle_whatsapp_message("491234567890", "I want to book an appointment with my doctor")
