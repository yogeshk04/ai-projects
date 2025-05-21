# BasicChatboat

A simple conversational chatbot built using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and large language models (LLMs) such as Google Gemini or Ollama.

## Features

- Interactive chat loop in the terminal
- Supports both Google Gemini and Ollama LLMs (switchable in code)
- Uses a state graph for managing conversation flow

## Setup

1. **Install dependencies:**

   ```sh
   pip install -r ../requirements.txt
   ```

2. **Set up environment variables:**

   Copy `.env.example` to `.env` in the project root and fill in your API keys.

   ```
   cp ../.env.example ../.env
   ```

   Make sure to set `GOOGLE_API_KEY` for Gemini or the appropriate variables for Ollama.

3. **Run the chatbot:**

   ```sh
   python basic_chatboat.py
   ```

## Usage

- Type your message and press Enter.
- Type `exit`, `quit`, or `q` to end the chat.

## Configuration

- To use Ollama instead of Gemini, uncomment the `OllamaLLM` line and comment out the `ChatGoogleGenerativeAI` line in [`basic_chatboat.py`](basic_chatboat.py).

## File Structure

- [`basic_chatboat.py`](basic_chatboat.py): Main chatbot implementation.

## License

This project is released under [The Unlicense](../LICENSE).