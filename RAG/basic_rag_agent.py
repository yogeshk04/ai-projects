from langchain_community.document_loaders import UnstructuredURLLoader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate




# Load environment variables from .env file
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llm = OpenAI(model="gpt-4")
urls = [
    "https://langchain-ai.github.io/langgraph/concepts/why-langgraph/",
    "https://langchain-ai.github.io/langgraph/agents/agents/",
]   

loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

print("Data loaded successfully.")
print("Number of documents loaded:", len(data))

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
docs = text_splitter.split_documents(data)

print("Documents split into chunks successfully.")
print("Number of chunks created:", len(docs))
# Print the first chunk
print("First chunk content:")

vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings())
#vectorstore = Chroma.from_documents(docs, embedding_function=GooglePalmEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.invoke("what is langchain?")

len(retrieved_docs)

# Print the first retrieved document
print(retrieved_docs[0].page_content)



system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "What kind of services they provide?"})
print(response["answer"])

