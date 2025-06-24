from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from ai_chatbot.core.intent_detection import detect_intent
from ai_chatbot.calendar_integration.calendar_api import get_free_slots, book_appointment

class ChatState:
    def __init__(self, messages, intent=None, slots=None):
        self.messages = messages
        self.intent = intent
        self.slots = slots

def check_calendar(state):
    state.slots = get_free_slots()
    return state

def suggest_slots(state):
    slot_text = "\n".join(state.slots)
    state.messages.append({"role": "assistant", "content": f"Available slots:\n{slot_text}"})
    return state

def confirm_booking(state):
    user_message = state.messages[-1]["content"]
    selected_slot = extract_slot_from_user(user_message, state.slots)
    if selected_slot:
        book_appointment(selected_slot)
        state.messages.append({"role": "assistant", "content": f"Appointment booked at {selected_slot}"})
    else:
        state.messages.append({"role": "assistant", "content": "Sorry, I couldn't understand the selected time."})
    return state

def extract_slot_from_user(text, slots):
    for slot in slots:
        if slot in text:
            return slot
    return None

graph = StateGraph(ChatState)
graph.add_node("detect_intent", detect_intent)
graph.add_node("check_calendar", check_calendar)
graph.add_node("suggest_slots", suggest_slots)
graph.add_node("confirm_booking", confirm_booking)

graph.set_entry_point("detect_intent")
graph.add_edge("detect_intent", "check_calendar")
graph.add_edge("check_calendar", "suggest_slots")
graph.add_edge("suggest_slots", "confirm_booking")
graph.set_finish_point("confirm_booking")

app = graph.compile()
