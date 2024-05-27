import psycopg2
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "enter api key here"

# Initialize OpenAI LLM with LangChain
llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0.3)

st.title("ParadeDB SQL Connect with Streamlit, LangChain, and OpenAI")

# Function to execute SQL commands on PostgreSQL
def execute_sql(command):
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
        conn.commit()

        # Fetch data if the command is a SELECT statement
        if command.strip().lower().startswith("select"):
            data = cur.fetchall()
        else:
            data = None

        return data

    except psycopg2.Error as e:
        st.error(f"Error executing SQL command: {e}")
        return None

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to generate SQL INSERT command using OpenAI and LangChain
def generate_insert_command(table_name, column_names, values):
    prompt = PromptTemplate.from_template(
        "Generate a SQL INSERT command to insert the values {values} into the columns {column_names} of the table {table_name}."
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    insert_command = chain.run(table_name=table_name, column_names=column_names, values=values)
    return insert_command

# Streamlit input for table name, columns, and values
table_name = st.text_input("Enter the table name:")
columns = st.text_input("Enter the column names (comma-separated):")
values = st.text_input("Enter the values (comma-separated):")

if st.button("Insert Data"):
    if table_name and columns and values:
        # Generate the SQL INSERT command
        insert_command = generate_insert_command(table_name, columns, values)

        # Display the generated command
        st.write(f"Generated SQL INSERT Command: {insert_command}")

        # Execute the generated command
        execute_sql(insert_command)

        # Fetch and display data after insertion
        fetch_command = f"SELECT * FROM {table_name};"
        data = execute_sql(fetch_command)
        if data:
            st.write("Data after insertion:")
            st.write(data)
        else:
            st.write("No data found or error fetching data.")
    else:
        st.error("Please enter the table name, columns, and values.")

