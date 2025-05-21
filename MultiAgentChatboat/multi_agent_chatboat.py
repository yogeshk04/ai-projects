from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize the Tavily search tool
search_tool = TavilySearchResults(seach_depth="basic")

# Initialize the DuckDuckGo search tool
search = DuckDuckGoSearchRun()

# Define a simple translation tool (mocked for now)
def translate(text):
    return f"[Translated to English] {text}"

# Define a summarization tool
def summarize(text):
    return f"[Summary] {text[:100]}..."

# Define a fact-checking tool using search
def fact_check(text):
    results = search.run(text)
    return f"[Fact-Check Results] {results[:200]}..."

# Define the LangGraph-style flow
def langgraph_chatbot(user_input):
    print("🔁 Translating...")
    translated = translate(user_input)

    print("📝 Summarizing...")
    summary = summarize(translated)

    print("🔍 Fact-checking...")
    facts = fact_check(summary)

    print("💬 Generating response...")
    prompt = PromptTemplate.from_template(
        "Based on the following summary and fact-check results, respond to the user:\n\nSummary:\n{summary}\n\nFacts:\n{facts}"
    )
    final_prompt = prompt.format(summary=summary, facts=facts)
    response = llm.predict(final_prompt)

    return response

# Example usage
if __name__ == "__main__":
    user_input = "Bonjour, pouvez-vous résumer cet article et vérifier les faits?"
    reply = langgraph_chatbot(user_input)
    print("\n🤖 Chatbot Response:\n", reply)
