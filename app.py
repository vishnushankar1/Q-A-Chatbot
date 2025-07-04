import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_v2'] = 'true'



#prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Hey act like an Q&A Chatbot please answer the following questions"),
        ("user","question : {question}")
    ]
)

def generate_response(question,llm,api_key,temperature,max_tokens):
    llms=ChatGroq(model=llm,groq_api_key=api_key)
    parser=StrOutputParser()
    chain=prompt | llms | parser
    res=chain.invoke({"question":question})
    return res

st.title("Enhanced Q&A chatbot with GroqAI")
st.sidebar.title('Settings')
api_key=st.sidebar.text_input("Groq API key",type='password',help='please sign up in this webiste and create your Api key at https://console.groq.com/key')
llm=st.sidebar.selectbox("Select your Groq AI Model",["gemma2-9b-it",'llama-3.3-70b-versatile','deepseek-r1-distill-llama-70b'])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=0,max_value=300,value=150)

st.write("hey! you can ask your questions here.")
input_text=st.text_input("You : ")

if input_text:
    if not api_key:
        st.write("Please enter your groq api key in the side bar")
    else:
        ans=generate_response(input_text,llm,api_key,temperature,max_tokens)
        st.write(ans)
elif not api_key:
    st.warning("please enter the api key in the side bar")
else:
    st.write("please provide the user input")

