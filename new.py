import streamlit as st
import csv
from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
from io import TextIOWrapper

app = Flask(__name__)

# Ngrok tunnel URL
ngrok_url = "https://8020-42-105-164-136.ngrok-free.app"

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "e97f5403f84e7352dc0638fa5659d772"
twilio_phone_number = "+12513166471"

# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Gather> verb to gather user's response
        response = VoiceResponse()
        gather = Gather(input='speech', action=f'{ngrok_url}/twilio/record_response', method='POST')
        gather.say("Hello! Do you have a requirement for cumin seeds? Please respond with yes or no.")
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

# Function to create a conference call between two numbers
def create_conference_call(dialed_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Dial> verb and <Conference> noun
        response = VoiceResponse()
        response.say("We are connecting you with Nilesh shortly.")
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
    try:
        recording_url = request.form.get("RecordingUrl")
        # Add your handling logic here
        return Response(status=200)
    except Exception as e:
        st.error(f"Error handling recorded response: {e}")
        return Response(status=500)

# Main function to run the Streamlit app
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
                # Open the file in text mode explicitly with UTF-8 encoding
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
                successful_calls += 1

        st.success(f"Calls made to {successful_calls} out of {len(phone_numbers)} phone numbers!")

# Streamlit app logic goes here
if __name__ == "__main__":
    main()
