import streamlit as st
from langchain_helper import get_sql_chain_response

st.title("AtliQ T Shirts: Database Q&A 👕")

question = st.text_input("Question: ")

if question:
    response = get_sql_chain_response(question)

    st.header("Answer")
    st.write(response)






