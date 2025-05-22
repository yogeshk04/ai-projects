from typing import Dict, TypedDict
# StarteGraph is a class that helps in building and managing state graphs for various applications.
from langgraph.graph import StateGraph

# Create an AgentState class that inherits from TypedDict
class AgentState(TypedDict):
    message: str
    
# Define the function to be executed in the state graph
def greeting_node(state: AgentState) -> AgentState:
    """ Siple node that returns a greeting message to the state. """    
    state["message"] = "Hello! " + state["message"] + ", how can I assist you today?"
    return state

