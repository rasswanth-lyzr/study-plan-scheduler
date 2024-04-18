import os
from lyzr import QABot
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

def get_files_in_directory(directory="data"):
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def rag_implementation():
    # Get the file path
    file_path = get_files_in_directory()[0]

    # Initialize the RAG Lyzr QABot
    rag = QABot.pdf_qa(
        input_files=[file_path],
        llm_params={"model": "gpt-4-turbo-preview"},
    )

    return rag


text_constraints = st.text_input("Enter your constraints")
button_clicked = st.button("OK")

if button_clicked:
    qa_bot = rag_implementation()
    prompt = f'''Input Description:
    The input will be a detailed course curriculum document. This document includes the following key components:

    Course title and description
    List of topics covered, including subtopics
    Duration of the course
    Total number of lecture hours
    Recommended readings and resources

    Output Requirements:
    Create a comprehensive study plan schedule that adheres to the following criteria:

    Overall Structure: The schedule should cover the course curriculum
    Daily Study Sessions: Recommend optimal daily study sessions considering a balance between productivity and well-being.
    Breaks and Downtime: Include short breaks within daily sessions and longer breaks between days of intensive study.

    Make sure the schedule sticks to the following constraints strictly : 
    {text_constraints}

    [!IMPORTANT] Always think before answering. Always explicitly generate the output. Do not skip or generalise. Do not exceed time constraints.
    '''
    response = qa_bot.query(prompt)
    st.markdown(f"""{response.response}""")