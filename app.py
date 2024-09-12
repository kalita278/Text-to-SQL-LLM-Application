import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

import pymysql


load_dotenv()


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_response(input,prompt):

    model = genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([prompt,input])

    return response.text


def sql_response(query,db):
    a = pymysql.connect(user='root',host='127.0.0.1',passwd='mrinal',db=db)
    cur = a.cursor()
    cur.execute(query)
    result = cur.fetchall()
    a.close()
    for i in result:
        print(i)
    return result

## Define Your Prompt
prompt= """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name sakila with table name actor. actor has the following columns - actor_id, first_name, last_name,last_update 
    \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this select count(*) from actor ;
    also the sql code should not have ``` in beginning or end and sql word in output
    """

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_response(question,prompt)
    print(response)
    response=sql_response(response,"sakila")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
