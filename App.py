import os
import streamlit as st
from groq import Groq

# Set your Groq API key
api_key = "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"

# Function to qualify leads using Groq API
def qualify_leads(messages):
    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)
    
    # Make API call to qualify leads using "mistral-8b" model
    chat_completion = client.chat.completions.create(messages=messages, model="mistral-8b")
    
    # Return the content of the response
    return chat_completion.choices[0].message.content

def main():
    st.title("AI Sales Agent")

    # File uploader to upload chat messages CSV file
    st.write("Upload CSV file with chat messages:")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Processing...")

        # Read chat messages from uploaded CSV file
        messages = []
        with uploaded_file as file:
            for line in file:
                messages.append({"role": "user", "content": line.strip()})

        # Qualify leads using Groq API
        response = qualify_leads(messages)

        # Display response from AI Sales Agent
        st.write("Response from AI Sales Agent:")
        st.write(response)

if __name__ == "__main__":
    main()
