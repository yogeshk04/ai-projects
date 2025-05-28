from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
import certifi

# Ensure that the certifi package is used for SSL certificates
os.environ["SSL_CERT_FILE"] = certifi.where()



# Load environment variables from .env file
load_dotenv()

# Define the AgentState TypedDict to represent the state of the agent
class AgentState(TypedDict):
    messages: List[HumanMessage]
    
# Initialize llm with OpenAI's Chat model
llm = ChatOpenAI(model="gpt-4o")
#llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Define the process function that will be used in the state graph
def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

# Initialize the state graph
stateGraph = StateGraph(AgentState)

# Add the process function as a node in the graph
stateGraph.add_node("process", process)

# Add edges to connect the START node to the process node and the process node to the END node
stateGraph.add_edge(START, "process")
stateGraph.add_edge("process", END)

# Compile the graph
agent = stateGraph.compile()


user_input = input("You: ")
while user_input.lower() != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("You: ")
# Print a message indicating the end of the conversation

