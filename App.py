import streamlit as st
import csv
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from io import TextIOWrapper

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "4148f2ba8b790520814a3395a83b841f"
twilio_phone_number = "+12513166471"

# Groq API key
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/analyze"

# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response
        response = VoiceResponse()
        gather = Gather(input='speech', action='http://your_domain.com/twilio/inbound_call', method='POST')
        gather.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
        response.append(gather)

        # Make call
        call = client.calls.create(
            twiml=response,
            to=phone_number,
            from_=twilio_phone_number,
            status_callback='http://your_domain.com/twilio/status',
            method='POST'
        )
        return call.sid
    except Exception as e:
        st.error(f"Error occurred while making call to {phone_number}: {e}")
        return None

# Function to handle response from call
def handle_response(response):
    try:
        user_response = response['SpeechResult']
        st.info(f"Response from user: {user_response}")
        
        # Generate follow-up question using Groq API
        follow_up_question = generate_follow_up_question(user_response)
        if follow_up_question:
            st.info(f"Follow-up question generated: {follow_up_question}")
        else:
            st.error("Failed to generate follow-up question")

        # Convert Groq response to voice and relay over Twilio
        convert_and_relay(user_response)
    except Exception as e:
        st.error(f"Error handling response: {e}")

# Function to generate follow-up question using Groq API
def generate_follow_up_question(text):
    try:
        headers = {"Authorization": f"Bearer {groq_api_key}"}
        data = {"text": text, "model": "llama3-8b-8192"}
        response = requests.post(groq_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            follow_up_question = response.json().get("follow_up_question", "")
            return follow_up_question
        else:
            st.error(f"Groq API request failed with status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error generating follow-up question: {e}")
        return None

# Function to convert text response to voice and relay over Twilio
def convert_and_relay(text):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        call = client.calls.create(
            to="+917415818295",  # Sales executive number
            from_=twilio_phone_number,
            twiml=f'<Response><Say>{text}</Say></Response>'
        )
        st.info("Response relayed to sales executive.")
    except Exception as e:
        st.error(f"Error relaying response to sales executive: {e}")

def main():
    st.title("AI Sales Agent")

    # File uploader to upload CSV file with phone numbers
    uploaded_file = st.file_uploader("Upload CSV file with phone numbers:", type="csv")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Processing...")

        # Read phone numbers from uploaded CSV file
        try:
            phone_numbers = []
            with uploaded_file as file:
                # Open the file in text mode explicitly
                reader = csv.reader(TextIOWrapper(file, encoding='utf-8'), delimiter=',')
                next(reader)  # Skip header row
                for row in reader:
                    phone_number = '+91' + row[-1].strip()  # Add country code and extract phone number from the last column
                    phone_numbers.append(phone_number)
        except Exception as e:
            st.error(f"Error occurred while reading CSV file: {e}")
            return

        # Make calls to each phone number
        successful_calls = 0
        for phone_number in phone_numbers:
            call_sid = make_call(phone_number)
            if call_sid:
                st.info(f"Call initiated to {phone_number}. Waiting for response...")
                # Implement logic to capture and handle user response here
                response = {}  # Placeholder for Twilio response, to be replaced with actual response
                handle_response(response)
                successful_calls += 1

        st.success(f"Calls made to {successful_calls} out of {len(phone_numbers)} phone numbers!")

if __name__ == "__main__":
    main()
