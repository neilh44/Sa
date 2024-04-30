import streamlit as st
import csv
from groq import Groq
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse
from io import TextIOWrapper

# Set your Groq API key
api_key = "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"

# Set your Twilio credentials
twilio_account_sid = "AC66a810449e6945a613d5161b54adf708"
twilio_auth_token = "fc81eeff7d15fe6f52bd297b54536640"
twilio_phone_number = "+12513166471"

# Function to qualify leads using Groq API
def qualify_leads(messages):
    try:
        # Initialize the Groq client with the API key
        client = Groq(api_key=api_key)
        
        # Make API call to qualify leads using "mistral-8b" model
        chat_completion = client.chat.completions.create(messages=messages, model="mistral-8b")
        
        # Return the content of the response
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error occurred while qualifying leads: {e}")
        return None

# Function to make a call using Twilio
def make_call(phone_number):
    try:
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
        return call.sid
    except Exception as e:
        st.error(f"Error occurred while making call to {phone_number}: {e}")
        return None

# Function to handle response from call
def handle_response(response):
    # Process response here
    print("Response from user:", response)

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
                reader = csv.reader(TextIOWrapper(file, 'rt', encoding='utf-8'), delimiter=',')
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
                handle_response(call_sid)
                successful_calls += 1

        st.success(f"Calls made to {successful_calls} out of {len(phone_numbers)} phone numbers!")

if __name__ == "__main__":
    main()
