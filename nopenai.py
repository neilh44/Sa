import streamlit as st
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai

# Set up Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "4c1c17b298f8d9691bb245e09f9e3a2e"
twilio_phone_number = "+12513166471"

# Set up OpenAI API key
openai.api_key = "sk-proj-S8WGhSfJxym2XqWNpwimT3BlbkFJ9emIl0E7r18vR6OKNvJg"

# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        
        # Create TwiML response with <Gather> verb to gather user's response
        response = VoiceResponse()
        gather = Gather(input='speech', action='/twilio-webhook', method='POST')
        gather.say("Hello! Please leave your message after the tone.")
        response.append(gather)
        
        # Make call
        call = client.calls.create(
            twiml=response,
            to=phone_number,
            from_=twilio_phone_number,
            method='GET'
        )
        return call.sid
    except Exception as e:
        st.error(f"Error occurred while making call to {phone_number}: {e}")
        return None

# Function to handle response from call
@st.cache
def transcribe_audio(audio):
    try:
        # Use OpenAI Whisper for real-time speech-to-text
        response = openai.Transcription.create(
            audio=audio,
            content_type="audio/mpeg"
        )
        return response['text']
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("Twilio Call Transcription")
    
    # Input field to enter phone number
    phone_number = st.text_input("Enter phone number to dial (include country code)")

    # Button to initiate call
    if st.button("Make Call"):
        if phone_number:
            call_sid = make_call(phone_number)
            if call_sid:
                st.success(f"Call initiated to {phone_number}.")
            else:
                st.error("Failed to initiate call.")
        else:
            st.warning("Please enter a phone number.")

# Streamlit app logic goes here
if __name__ == "__main__":
    main()
