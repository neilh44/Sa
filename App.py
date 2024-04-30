import os
import streamlit as st
import csv
from groq import Groq
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse

# Set your Groq API key
api_key = "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"

# Set your Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "a53cd4fa4b79ad87f3f5ecaec10a34d6"
twilio_phone_number = "+12513166471"

# Function to qualify leads using Groq API
def qualify_leads(messages):
    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)
    
    # Make API call to qualify leads using "mistral-8b" model
    chat_completion = client.chat.completions.create(messages=messages, model="mistral-8b")
    
    # Return the content of the response
    return chat_completion.choices[0].message.content

# Function to make a call using Twilio
def make_call(phone_number):
    client = Client(twilio_account_sid, twilio_auth_token)

    # Create TwiML response
    response = VoiceResponse()
    gather = Gather(input='speech', action='/handle-response')
    gather.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
    response.append(gather)

    # Make call
    call = client.calls.create(
        twiml=response,
        to=phone_number,
        from_=twilio_phone_number
    )

# Function to handle response from call
def handle_response(response):
    # Process response here
    print("Response from user:", response)

def main():
    st.title("AI Sales Agent")

    # File uploader to upload CSV file with phone numbers
    st.write("Upload CSV file with phone numbers:")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Processing...")

        # Read phone numbers from uploaded CSV file
        phone_numbers = []
        with uploaded_file as file:
            reader = csv.reader(file, delimiter=',')  # Specify delimiter if needed
            for row in reader:
                phone_numbers.append(row[0])

        # Make calls to each phone number
        for phone_number in phone_numbers:
            make_call(phone_number)

        st.write("Calls made to phone numbers!")
