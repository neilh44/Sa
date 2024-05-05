import streamlit as st
import csv
from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from io import TextIOWrapper
import requests

app = Flask(__name__)

# Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "4c1c17b298f8d9691bb245e09f9e3a2e"
twilio_phone_number = "+12513166471"

# Groq API key and endpoint
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/analyze"

# Function to make a call using Twilio
def make_call(phone_number):
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        # Create TwiML response with <Gather> verb to gather user's response
        response = VoiceResponse()
        gather = Gather(input='speech', action='/twilio-webhook', method='POST')
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

# Function to analyze user response using Groq
def analyze_user_response(user_response):
    try:
        # Analyze user response using Groq
        groq_payload = {
            "analyze": {
                "text": user_response,
                "queries": [
                    {
                        "intent": {
                            "name": "cumin_seeds_requirement",
                            "examples": ["yes", "no"]
                        }
                    }
                ]
            }
        }
        response = requests.post(groq_endpoint, json=groq_payload, headers={"Authorization": f"Bearer {groq_api_key}"})
        response_data = response.json()

        # Get the intent detected by Groq
        intent = response_data['results']['analyze']['intents'][0]['name']

        # Process the intent and return response message
        if intent == "cumin_seeds_requirement":
            if user_response.lower() == "yes":
                return "Great! We have a variety of cumin seeds available. How many kilograms do you need?"
            elif user_response.lower() == "no":
                return "No problem. If you have any other requirements, feel free to let us know."
            else:
                return "Sorry, I didn't understand your response. Can you please say 'yes' or 'no'?"
    except Exception as e:
        st.error(f"Error analyzing user response: {e}")
        return "Sorry, something went wrong while processing your request."

# Function to handle response from call or SMS
@app.route("/twilio-webhook", methods=["POST"])
def handle_twilio_webhook():
    try:
        # Check if the request is a voice call or an SMS
        if request.values.get('SpeechResult'):
            user_response = request.values.get('SpeechResult')
            # Handle voice call response
            print(f"User's voice response: {user_response}")
        else:
            # Handle SMS response
            user_response = request.values.get('Body')
            print(f"User's SMS response: {user_response}")

        # Analyze user response
        response_message = analyze_user_response(user_response)

        # Respond with TwiML response
        twilio_response = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say>{response_message}</Say>
        </Response>
        """

        return twilio_response, 200
    except Exception as e:
        st.error(f"Error handling Twilio webhook: {e}")
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
