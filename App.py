import streamlit as st
import csv
from flask import Flask, request, Response
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from io import TextIOWrapper

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "your_auth_token"
twilio_phone_number = "your_twilio_phone_number"
twilio_auth_token = "fc0b6f2111b1736b7947be673e5c7101"
twilio_phone_number = "+12513166471"

# Groq API key
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/analyze"

# Function to make a call to a given phone number
# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Gather> verb to gather user's response
        # Create TwiML response
        response = VoiceResponse()
        gather = Gather(input='speech', action='/twilio/record_response', method='POST')
        gather = Gather(input='speech', action='http://nileshhanotia.pythonanywhere.com/twilio/inbound_call', method='POST')
        gather.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
        response.append(gather)

@@ -32,27 +35,67 @@ def make_call(phone_number):
        )
        return call.sid
    except Exception as e:
        print(f"Error occurred while making call to {phone_number}: {e}")
        st.error(f"Error occurred while making call to {phone_number}: {e}")
        return None

# Function to create a conference call between two numbers
def create_conference_call(dialed_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Dial> verb and <Conference> noun
        response = VoiceResponse()
        dial = Dial()
        dial.conference("SalesConference", beep='false', end_conference_on_exit='true')
        response.append(dial)

        # Make a call to the dialed number and add to conference
        call = client.calls.create(
            to=dialed_number,
            from_=twilio_phone_number,
            twiml=response
        )
        return call.sid
    except Exception as e:
        st.error(f"Error occurred while creating conference call: {e}")
        return None

# Function to handle recorded response from call
@app.route("/twilio/record_response", methods=["POST"])
def handle_recorded_response():
# Function to handle response from call
def handle_response(response):
    try:
        recording_url = request.form.get("RecordingUrl")
        # Add your handling logic here
        return Response(status=200)
        # Check if the response contains the user's speech input
        if 'SpeechResult' in response:
            user_response = response['SpeechResult']
            st.info(f"Response from user: {user_response}")

            # If user responds with "yes", create a conference call
            if user_response.lower() == "yes":
                conference_call_sid = create_conference_call("+917046442667")
                if conference_call_sid:
                    st.info("Conference call initiated.")
                else:
                    st.error("Failed to initiate conference call.")
            else:
                # Generate follow-up question using Groq API
                follow_up_question = generate_follow_up_question(user_response)
                if follow_up_question:
                    st.info(f"Follow-up question generated: {follow_up_question}")
                else:
                    st.error("Failed to generate follow-up question")

                # Convert Groq response to voice and relay over Twilio
                convert_and_relay(user_response)
        else:
            st.error("No speech input found in response. Please speak clearly and try again.")
    except Exception as e:
        print(f"Error handling recorded response: {e}")
        return Response(status=500)
        st.error(f"Error handling response: {e}")

# Main function to run the Streamlit app
def main():
    st.title("AI Sales Agent")

    # File uploader to upload CSV file with phone numbers
    uploaded_file = st.file_uploader("Upload CSV file with phone numbers:", type="csv")

    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Processing...")
@@ -61,7 +104,7 @@ def main():
        try:
            phone_numbers = []
            with uploaded_file as file:
                # Open the file in text mode explicitly
                # Open the file in text mode explicitly with UTF-8 encoding
                reader = csv.reader(TextIOWrapper(file, encoding='utf-8'), delimiter=',')
                next(reader)  # Skip header row
                for row in reader:
@@ -84,6 +127,5 @@ def main():

        st.success(f"Calls made to {successful_calls} out of {len(phone_numbers)} phone numbers!")

# Streamlit app logic goes here
if __name__ == "__main__":
    main()
