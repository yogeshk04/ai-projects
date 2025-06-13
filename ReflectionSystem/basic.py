from typing import List, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import MessageGraph, END
from chains import generate_chain, reflection_chain

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"

graph = MessageGraph()

def generate_node(state):
    return generate_chain.invoke({
        "messages": state
    })

def reflect_node(messages):
    response = reflection_chain.invoke({
        "messages": messages
    })
    return [HumanMessage(content=response.content)]

graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if (len(state) > 3):
        return END    
    return REFLECT

graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

response = app.stream([HumanMessage(content="Write a tweet about LangGraph")])

print(response)
