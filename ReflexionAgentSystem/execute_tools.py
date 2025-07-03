import json
from typing import Any, Dict, List
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from langchain_community.tools import TavilySearchResults

# create tavily search tool
tavili_tool = TavilySearchResults(max_results=5)

# function to execute search queries from AnswerQuestion tool calls
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message = AIMessage = state[-1]

    # Execute tools calls from the last AI message
    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        return []
    
    # Process the AnswerQuestion or ReviseAnswer tool calls to extract search queries
    tool_messages = []

    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries", [])

            # Execute each search query using the Tavily tool
            query_results = {}
            for query in search_queries:
                results = tavili_tool.invoke(query)
                query_results[query] = results
            
            # Create a ToolMessage for each search query result
            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id                    
                )
            )
    return tool_messages

# Example usage
test_state = [
    HumanMessage(
        content="What are the benefits of using AI in small businesses?"
    ),
    AIMessage(
        content="Here is a detailed answer to your question.",
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "args": {
                    "answer": "",
                    "search_queries": [
                        "AI Tools for small business",
                        "AI in samll business making",
                        "AI automation for small business"
                    ],
                    "reflection": {
                        "missing": "",
                        "superfluous": ""
                    }
                },
                "id": "tool_call_1"
            }
        ],
    )


]
        

            