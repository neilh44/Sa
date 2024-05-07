from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from io import BytesIO, TextIOWrapper
import streamlit as st
from groq import Groq

app = Flask(__name__)

# Ngrok tunnel URL
https://d7eb-103-85-8-165.ngrok-free.app/

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "4c1c17b298f8d9691bb245e09f9e3a2e"
twilio_phone_number = "+12513166471"

# Groq API key
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/analyze"

# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Record> verb to record user's response
        response = VoiceResponse()
        response.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
        response.record(action="/twilio/record_response", method="POST", max_length=10)  # Recording maximum of 10 seconds

        # Make call
        call = client.calls.create(
            twiml=response,
            to=phone_number,
            from_=twilio_phone_number,
            status_callback='http://nileshhanotia.pythonanywhere.com/twilio/status',
            method='POST'
        )
        return call.sid
    except Exception as e:
        st.error(f"Error occurred while making call to {phone_number}: {e}")
        return None

# Function to handle recorded response from call
def handle_recorded_response(recording_url):
    try:
        # Download the recorded audio
        response = requests.get(recording_url)
        audio_data = BytesIO(response.content)

        # Placeholder for determining user's intent
        user_intent = "buy"  # Assuming user's intent is to buy

        # Generate follow-up questions based on user's intent
        follow_up_questions = generate_follow_up_questions(user_intent)

        # Convert and relay follow-up questions over Twilio
        for question in follow_up_questions:
            convert_and_relay(question)
    except Exception as e:
        st.error(f"Error handling recorded response: {e}")

# Function to generate follow-up questions based on user's intent
def generate_follow_up_questions(user_intent):
    follow_up_questions = []
    if user_intent == "buy":
        follow_up_questions.append("What quantity of cumin seeds do you need?")
        follow_up_questions.append("Do you have any specific quality requirements?")
        follow_up_questions.append("Where would you like the delivery to be made?")
        follow_up_questions.append("What price range are you looking at?")
    return follow_up_questions

# Function to convert Groq response to voice and relay over Twilio
def convert_and_relay(message):
    try:
        # Use Groq API to generate response based on selected model
        client = Groq(api_key=groq_api_key)
        response = client.analyze.create(text=message, model="llama3-70b-8192")
        generated_response = response.output.text

        # Create TwiML response to relay generated response over Twilio call
        twiml_response = VoiceResponse()
        twiml_response.say(generated_response)

        # Return TwiML response
        return str(twiml_response)
    except Exception as e:
        st.error(f"Error converting and relaying message: {e}")
        return None

# Streamlit app
def main():
    st.title("AI Sales Agent")

    # Form to input phone number
    phone_number = st.text_input("Enter phone number (with country code):")

    # Button to initiate call
    if st.button("Make Call"):
        call_sid = make_call(phone_number)
        if call_sid:
            st.info(f"Call initiated to {phone_number}. Waiting for response...")

if __name__ == "__main__":
    main()
