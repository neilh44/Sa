import streamlit as st
import csv
import requests
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say
from io import TextIOWrapper

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "186ac9b8de4b75fc5e36fe41e05d4bb3"
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
        gather = Gather(input='speech', action='http://nileshhanotia.pythonanywhere.com/twilio/inbound_call', method='POST')
        gather.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
        response.append(gather)

        # Make call
        call = client.calls.create(
            twiml=response,
            url='https://2668-2402-3a80-1ce6-eb09-2934-12a8-91f2-d90a.ngrok-free.app/twilio-webhook',  # Ngrok URL for Twilio webhook endpoint
            to=phone_number,
            from_=twilio_phone_number,
            status_callback='http://nileshhanotia.pythonanywhere.com/twilio/status',
            method='POST'
            method='GET'
        )
        return call.sid
    except Exception as e:
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

# Function to handle response from call
def handle_response(response):
    try:
@@ -70,7 +35,8 @@ def handle_response(response):

            # If user responds with "yes", create a conference call
            if user_response.lower() == "yes":
                conference_call_sid = create_conference_call("+917046442667")
                st.info("Initiating conference call...")
                conference_call_sid = create_conference_call("+917046442677")
                if conference_call_sid:
                    st.info("Conference call initiated.")
                else:
@@ -90,6 +56,27 @@ def handle_response(response):
    except Exception as e:
        st.error(f"Error handling response: {e}")

def create_conference_call(dialed_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Dial> verb and <Conference> noun
        response = VoiceResponse()
        response.say("We are connecting you with Nilesh shortly.")
        dial = response.dial()
        dial.conference("SalesConference", beep='false', end_conference_on_exit='true')

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

def main():
    st.title("AI Sales Agent")
