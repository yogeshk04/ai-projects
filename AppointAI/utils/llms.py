import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

class LLMModels:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        if not model_name:
            raise ValueError("Model name must be provided.")
        self.model_name = model_name
        self.openai_model=ChatGoogleGenerativeAI(model=self.model_name)

    def get_model(self):
        return self.openai_model
    

if __name__ == "__main__":
    llm_instance = LLMModels()
    llm_model = llm_instance.get_model()
    response = llm_model.invoke("Hello")
    print(response.content)  # Print the last message content

