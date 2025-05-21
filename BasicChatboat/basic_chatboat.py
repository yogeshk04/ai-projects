# pip install --upgrade langchain-community langgraph
# pip install langchain-ollama

from typing import Any, List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Step 1: Define state graph
class State(Dict):
    messages: List[Dict[str, str]]
    
# Step 2: Initialize the state graph
graph_builder = StateGraph(State)

# Step 3: Initialize the LLM
#llm = OllamaLLM(model="llama3.1")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Step 4: Define the chat function
def chat_function(state: State):
    response = llm.invoke(state["messages"])
    # For Google Generative AI, extract only the content attribute
    try:
        content = response.content  # Only the text reply
    except AttributeError:
        # fallback for dict or other types
        if isinstance(response, dict) and "content" in response:
            content = response["content"]
        else:
            content = str(response)
    state["messages"].append({"role": "assistant", "content": content})
    return {"messages": state["messages"]}

# Step 5: Add nodes and edges to the graph
graph_builder.add_node("chat", chat_function)
graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", END)

# Step 6: Compile the graph
graph = graph_builder.compile()

# Step 7: Stream graph updates
def stream_graph_updates(user_input: str):
    # Step 8: Initialize the state with user input
    state = {"messages": [{"role": "user", "content": user_input}]}
    for event in graph.stream(state):
        for value in event.values():
            # print the Chatboat's response
            print("Chatboat: ", value["messages"][-1]["content"])

# Step 9: Run the chat function in a loop
if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting the chat. Goodbye!")
                break
            # Step 10: Stream graph updates with user input
            stream_graph_updates(user_input)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        
# Note: This code is a simplified example and may require additional error handling and validation for production use.
# The code uses the LangGraph library to create a state graph for a chat application using the Ollama LLM.
# The graph is built with nodes and edges, and the chat function is defined to handle user input and generate responses.
# The graph is then compiled, and the chat function is run in a loop to allow for continuous interaction with the user.
# The user can exit the chat by typing "exit", "quit", or "q".
# The code also includes error handling to catch any exceptions that may occur during execution.
# The code is designed to be run in a Python environment with the necessary libraries installed.
# The code uses the Ollama LLM model "llama3.1" for generating responses to user input.
# The code also uses the ChatGoogleGenerativeAI model "gemini-2.0-flash" as an alternative LLM.

