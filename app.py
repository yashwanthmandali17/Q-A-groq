import streamlit as st 
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os 

load_dotenv()

# Langsmith Tracking

os.environ["groq_api_key"] = os.getenv("groq_api_key")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["langchain_project"] = os.getenv("langchain_project")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question: {question}")
    ]
)

# Function to generate a response

def generate_response(question, model_name, temperature, max_tokens):
    llm = ChatGroq(
        model = model_name,
        groq_api_key = os.getenv("groq_api_key"),
        temperature=temperature,
        max_tokens=max_tokens
    )

    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})
    return answer

# Streamlit UI

st.title("QnA chatbot with Groq")

# Sidebar
st.sidebar.title("Settings")

# Select the Groq models
model_name = st.sidebar.selectbox(
    "Select Groq Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",

    ]
)

#Parameters

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value = 50,
    max_value = 1000,
    value = 300,
)

# User Input
st.write("Go ahead and ask any question")

user_input = st.text_input("You:")

if user_input:
    response = generate_response(
        user_input,
        model_name,
        temperature,
        max_tokens
    )

    st.write(response)
else:
    st.write("Please provide user input.")