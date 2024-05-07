import os
import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

def main():

    load_dotenv()

    st.set_page_config(page_title="Ask your CSV 📁")
    st.header("Ask your CSV 📁")
    st.markdown("You can either use the default CSV file that comes with this demo, or upload your own.")
    st.markdown("Example usage:")
    st.markdown(''':red[1.] How many entries does the file contain?''')
    st.markdown(''':red[1.] What is the mean radius of the malignant tumors??''')
    st.markdown(''':red[1.] Give a summary about any patterns in the file''')

    user_csv = "data.csv"
    col1, col2 = st.columns(2)
    if col1.button("Use default .csv", type="primary"):
        user_csv = "data.csv"
    if col2.button("Upload your own .csv file"):
        user_csv = st.file_uploader("Upload your CSV file", type="csv")
    
    

    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV")
        if user_question is not None and user_question != "":
            with st.spinner("Fetching answer..."):
                llm = OpenAI(temperature=0)
                agent = create_csv_agent(llm, user_csv, verbose=True)
                response = agent.run(user_question)
            st.write(response)

            
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

if __name__ == "__main__":
    main()