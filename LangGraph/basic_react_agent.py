from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv()

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize the Tavily search tool
search_tool = TavilySearchResults(seach_depth="basic")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S" ):
    """  Get the current system time in the specified format. """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool, get_system_time]
# Initialize the agent with the Google Generative AI model and the search tool
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True)

agent.invoke("When the Chandrayaan-3 was launch and how many days ago was the from this instant?") 