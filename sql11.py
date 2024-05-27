import psycopg2
import openai
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.chains import LLMChain

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "enter api key here"

# Initialize OpenAI LLM with LangChain
llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0.3)

st.title("ParadeDB SQL Connect with Streamlit, LangChain, and OpenAI")

# Function to fetch data from PostgreSQL
def fetch_data(command):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            user="krishna",
            password="simple",
            host="localhost",
            port="5432",
            database="krishnadb"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL command
        cur.execute(command)
        data = cur.fetchall()

        # Commit the transaction if needed
        conn.commit()

        return data

    except psycopg2.Error as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return []

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

# Streamlit input for SQL command
command_input = st.text_input("Enter the SQL command:")

if st.button("Run Command"):
    if command_input:
        # Prompt template for LangChain
        prompt = PromptTemplate.from_template("{command} in SQL command only give one suitable output")

        # Create a LangChain LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate the SQL command using OpenAI
        generated_command = chain.run(command=command_input)

        # Display the generated command
        st.write(f"Generated SQL Command: {generated_command}")

        # Fetch data from PostgreSQL using the generated command
        data = fetch_data(generated_command)

        # Display the data in Streamlit
        if data:
            st.write("Data fetched from PostgreSQL:")
            st.write(data)
        else:
            st.write("No data found or error fetching data.")
    else:
        st.error("Please enter a SQL command.")

# Example usage:
if __name__ == "__main__":
    data = fetch_data("SELECT * FROM Tour;")
    if data:
        print(data)
