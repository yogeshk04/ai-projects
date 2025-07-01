from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

pydantic_parser = PydanticToolsParser(
    tools=[AnswerQuestion]
)

# Actor Agent Prompt Template
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researchr.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Ne server to maximize improvements,
3. After teh reflection, **list 1-3 serarch queries separately*** for
researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time = lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = "Provide a detailed ~250 word answer to the question, including relevant context and examples."
)

#llm = ChatOpenAI("gpt-4o")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

first_responder_chain = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion") | pydantic_parser

response = first_responder_chain.invoke({
    "messages": [
        HumanMessage(
            content="Write me a blog post on how small business can leverage AI to grow"
        )
    ]    
})

print(response)