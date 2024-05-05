import streamlit as st
from RealtimeSTT import RealtimeSTT
from twilio.rest import Client

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "4c1c17b298f8d9691bb245e09f9e3a2e"
twilio_phone_number = "+12513166471"

# Initialize RealtimeSTT
realtime_stt = RealtimeSTT()

# Initialize Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

# Streamlit UI
st.title("Twilio Call Transcription")

# Make a call
if st.button("Make Call"):
    call = client.calls.create(
        twiml='<Response><Say>Start of call</Say></Response>',
        to='recipient_phone_number',
        from_=twilio_phone_number
    )
    st.write("Call initiated. Waiting for transcription...")

# Display live transcription
st.write("Live Transcription:")
transcription = realtime_stt.get_transcription()
st.write(transcription)

# Download transcript
if st.button("Download Transcript"):
    # Code to download transcript
    pass
