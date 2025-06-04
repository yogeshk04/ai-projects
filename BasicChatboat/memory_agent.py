import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage, AIMessage]

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    """This node will solve teh request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("Current State:", state["messages"])
    
    return state

stateGraph = StateGraph(AgentState)
stateGraph.add_node("process", process)
stateGraph.add_edge(START, "process")
stateGraph.add_edge("process", END)

agent = stateGraph.compile()

convesation_hostory = []

user_input = input("Enter: ")
while user_input != "exit":
    convesation_hostory.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": convesation_hostory})
    convesation_hostory = result["messages"]
    user_input = input("Enter: ")

with open("logging.txt", "w") as file:
    file.write("Your Conversation log:\n")

    for message in convesation_hostory:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")