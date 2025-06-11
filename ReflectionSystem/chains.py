from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

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

llm = ChatOpenAI(temperature=0.7, model="gpt-4o")

generate_prompt = generate_prompt | llm
reflection_prompt = reflection_prompt | llm