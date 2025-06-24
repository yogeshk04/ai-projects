from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import os
from openai import AzureOpenAI
import certifi
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Ensure that the certifi package is used for SSL certificates
os.environ["SSL_CERT_FILE"] = certifi.where()

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-10-21",
#     azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
#     )

# llm = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_version="2024-10-21",
#     #model="gpt-4o"  # Replace with your Azure OpenAI deployment name
# )
    
llm = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-10-21",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

generate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a twitter techie influencer assistant tasked with wtriting a tweet excellent twitter posts."
         "Generate the best twitter post possible for the user's request."
         "If the user provides critique, respond with a revised version of your vprevious attempts.",
         ),         
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# pritn the type of the generate_prompt

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
        "You are a viral twitter influncer grading a tweet. Generate critique and recommendations for the user's tweet."
        "Always provide detailed recommendations, including requests for length, virality, style etc."        
        ),  
        MessagesPlaceholder(variable_name="messages"),

    ]
)

generate_prompt = generate_prompt | llm
reflection_prompt = reflection_prompt | llm