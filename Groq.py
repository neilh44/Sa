import streamlit as st
from groq import Groq

# Set your Groq API key
api_key = "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"

# Create a dictionary to map model names to their corresponding max tokens
models = {
    "llama3-70b-8192": 8192,
    "llama3-8b-8192": 8192,
    "llama2-70b-4096": 4096,
    "mixtral-8x7b-32768": 32768,
    "gemma-7b-it": 8192
}

# Function to interact with Groq API and get chat response
def get_chat_response(messages, model):
    try:
        # Initialize the Groq client with the API key
        client = Groq(api_key=api_key)
        
        # Make API call to get chat response using the selected model
        chat_completion = client.chat.completions.create(messages=messages, model=model)
        
        # Return the content of the response
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
def main():
    st.title("Chat with Groq AI")

    # Select model
    selected_model = st.selectbox("Select Model", list(models.keys()))

    # User input
    user_input = st.text_input("User Input")

    # Button to send message
    if st.button("Send"):
        # Get chat response
        chat_response = get_chat_response([{"role": "user", "content": user_input}], selected_model)
        
        # Display chat response
        st.text_area("Chat Response", value=chat_response, height=200)

if __name__ == "__main__":
    main()
  
