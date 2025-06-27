from typing import Literal, Any
from langchain_core.tools import tool
from langgraph.types import Command
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langchain_core.prompts.chat import ChatPromptTemplate
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from prompt_library.prompt import system_prompt
from utils.llms import LLMModels
from toolkit.toolkits import *

class Router(TypedDict):
    next: Literal["information_node", "booking_node", "FINISH"]
    reasoning: str

class AgentState(TypedDict):
    messages: Annotated[list[Any], add_messages]
    id_number: int
    next: str
    query: str
    current_reasoning: str

class DoctorAppointmentAgent:
    def __init__(self):
        llm_model = LLMModels()
        self.llm = llm_model.get_model()

    def supervisor_node(self, state: AgentState) -> Command[Literal['information_node', 'booking_node', '__end__']]:
        print("------------------------- Below is the state right after entering -------------------------")
        print(state)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"user's identificatioin number is {state['id_number']}, and the query is {state['query']}"},
        ] + state['messages']

        print("------------------------- Below is the messages right after entering -------------------------")
        print(messages)

        query = ''
        if len(state["messages"]) == 1:
            query = state["messages"][0].content

        print("------------------------- Below is the query right after entering -------------------------")
        print(query)

        response = self.llm_model.with_structured_output(Router).invoke(messages)

        goto = response['next']

        print("------------------------- This is my goto -------------------------")
        print(goto)

        print("------------------------- *** -------------------------")
        print(response["reasoning"])

        if goto == "FINISH":
            goto = END

        print("------------------------- Below is my state -------------------------")
        print(state)

        if query:
            return Command(goto=goto, update={
                'next': goto,
                'query': query,
                'current_reasoning': response["reasoning"],
                'messages': [HumanMessage(content=f"users's identification number is {state['id_number']}")]
                })
        return Command(goto=goto, update={
            'next': goto,
            'current_reasoning': response["reasoning"]}
            )
    
    def information_node(self, state: AgentState) -> Command[Literal['supervisor']]:
        print("------------------------- Called information node -------------------------")

        system_prompt = "You are specialized agent to provide information related to availability of doctors or any FAQs related to hospital based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2024."

        system_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("paceholder", "{messages}"),
            ]
        )

        information_agent = create_react_agent(
            model=self.llm_model.get_model(),
            tools=[check_availability_by_doctor, check_availability_by_specialization], prompt=system_prompt
        )

        result = information_agent.invoke(state)

        return Command(
            update={
                'messages': state['messages'] + [AIMessage(content=result['message'][-1].content, name='information_node')
                ]
            },
            goto="supervisor",
        )
    
    def booking_node(self, state: AgentState) -> Command[Literal['supervisor']]:
        print("------------------------- Called booking node -------------------------")

        system_prompt = "You are specialized agent to book appointment with doctor based on the query. You have access to the tool.\n Make sure to ask user politely if you need any further information to execute the tool.\n For your information, Always consider current year is 2024."

        system_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("paceholder", "{messages}"),
            ]
        )

        booking_agent = create_react_agent(
            model=self.llm_model.get_model(),
            tools=[set_appointment, cancel_appointment, reschedule_appointment], prompt=system_prompt
        )

        result = booking_agent.invoke(state)

        return Command(
            update={
                'messages': state['messages'] + [AIMessage(content=result['message'][-1].content, name='booking_node')]
            },
            goto="supervisor",
        )
    
    def build_graph(self):
        self.graph = StateGraph(AgentState)
        self.graph.add_node("supervisor", self.supervisor_node)
        self.graph.add_node("information_node", self.information_node)
        self.graph.add_node("booking_node", self.booking_node)
        self.graph.add_edge(START, "supervisor")
        self.app = self.graph.compile()
        return self.app
        

