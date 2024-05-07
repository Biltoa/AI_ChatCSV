import os
import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import pandas as pd

def update_api_key(new_key):
    os.environ["OPENAI_API_KEY"] = new_key


def main():

    load_dotenv()

    st.set_page_config(page_title="Ask your CSV 📁")
    st.header("Ask your CSV 📁")
    st.markdown("You can either use the example CSV file that comes with this demo, or upload your own.")
    st.markdown("Example usage:")
    st.markdown(''':red[1.] How many entries does the file contain?''')
    st.markdown(''':red[2.] What is the mean radius of the malignant tumors??''')
    st.markdown(''':red[3.] Give a summary about any patterns in the file''')

    st.markdown(''':red[Example CSV file below]''')

    data = pd.read_csv("data.csv")

    st.download_button(
        label="Download example CSV",
        data=data.to_csv().encode("utf-8"),
        file_name="data.csv",
        mime="text/csv",
    )
    
    new_api_key = st.text_input("Insert your OpenAI API key", os.getenv("OPENAI_API_KEY", ""))
    
    submit_button = st.button("Submit")
    if submit_button:
        update_api_key(new_api_key)
        st.success("OPENAI_API_KEY updated successfully!")

    st.divider()
    
    if os.getenv("OPENAI_API_KEY"):
        user_csv = st.file_uploader("Upload your CSV file", type="csv")


    if os.getenv("OPENAI_API_KEY") and user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV")
        submitQ_button = st.button("Submit Question")
        if submitQ_button and user_question is not None and user_question != "":
            with st.spinner("Fetching answer..."):
                llm = OpenAI(temperature=0)
                agent = create_csv_agent(llm, user_csv, verbose=True)
                response = agent.run(user_question)
            st.write(response)

    st.text(" ")
    st.text(" ")
    st.text(" ")
            
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

if __name__ == "__main__":
    main()