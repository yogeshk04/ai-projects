from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from openai import OpenAI
from google_calandar import get_free_slots, book_appointment

def extract_intent(message_content):
    # Dummy implementation: replace with actual intent extraction logic
    # For example, use simple keyword matching or an NLP model
    if "book" in message_content.lower():
        return "book_appointment"
    elif "available" in message_content.lower() or "free" in message_content.lower():
        return "check_availability"
    else:
        return "unknown"

# Define state
class ChatState:
    def __init__(self, messages=[], intent=None, slots=None):
        self.messages = messages
        self.intent = intent
        self.slots = slots

# Define nodes
def detect_intent(state: ChatState):
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=state.messages
    )
    state.intent = extract_intent(response.choices[0].message.content)
    return state

def check_calendar(state: ChatState):
    state.slots = get_free_slots()
    return state

def suggest_slots(state: ChatState):
    state.messages.append({"role": "assistant", "content": f"Available slots: {state.slots}"})
    return state

def confirm_booking(state: ChatState):
    selected_slot = extract_slot_from_user(state.messages)
    book_appointment(selected_slot)
    state.messages.append({"role": "assistant", "content": f"Appointment booked at {selected_slot}"})
    return state

# Build graph
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
