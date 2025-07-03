from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import MessageGraph, END

from chains import first_responder_chain, revisor_chain
from execute_tools import execute_tools

graph = MessageGraph()
MAX_ITERATIONS = 2

graph.add_node("draft_answer", first_responder_chain,)
graph.add_node("execute_tools", execute_tools)
graph.add_node("revise_answer", revisor_chain)

graph.add_edge("draft_answer", "execute_tools")
graph.add_edge("execute_tools", "revise_answer")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations >= MAX_ITERATIONS:
        return END
    return "execute_tools"

graph.add_conditional_edges("revise_answer", event_loop)
graph.set_entry_point("draft_answer")

app = graph.compile()

print(app.get_graph().draw_mermaid())

response = app.invoke(
    "Write about how small businesses can leverage AI to grow their business."
)

print(response[-1].tool_calls[0]["args"]["answer"])
print(response, "response")


