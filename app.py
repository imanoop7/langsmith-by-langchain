import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "TEST LLM"


if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]


st.set_page_config(page_title="Streming Bot")

st.title("Streaming Bot")

def get_response(query,chat_history):
    template= """
    You are helpful assistant. Answer  the following question considering the 
    Chat history:{chat_history}
    user question:{query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    chain = prompt |llm | StrOutputParser()

    return chain.stream(
        {
            "chat_history": chat_history,
            "user_question":query
        }
    )



for message in st.session_state.chat_history:
    if isinstance(message,HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)


user = st.chat_input("Your Message")
if user is not None and user !="":
    st.session_state.chat_histpry.append(HumanMessage(user))

    with st.chat_message("Human"):
        st.markdown(user)

    with st.chat_message("AI"):
        ai_response=st.write_stream(get_response(user,st.session_state.chat_history))
    
    st.session_state.chat_history.append(AIMessage(ai_response))




