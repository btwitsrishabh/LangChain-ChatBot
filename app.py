import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Calling environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Ensure the API keys are set
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    st.error("OPENAI_API_KEY not found in environment variables")

if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
else:
    st.error("LANGCHAIN_API_KEY not found in environment variables")

# Creating a chatbot prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in several fields. please provide response to the following user's query"),
        ("user", "Question:{question}"),
    ]
)

# Initialize Streamlit UI
st.title("Langchain Chatbot")
st.write("This is a chatbot that can answer your questions. Please type your question below.")
input_text = st.text_input("Enter your question here", "")

# Initialize the OpenAI chatbot
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# Create a chain
chain = prompt | llm | output_parser

# Displaying the response
if input_text:
    try:
        response = chain.invoke({"question": input_text})
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
