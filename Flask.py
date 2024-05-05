from flask import Flask, request
import requests

app = Flask(__name__)

# Twilio credentials
twilio_account_sid = "your_twilio_account_sid"
twilio_auth_token = "your_twilio_auth_token"
twilio_phone_number = "your_twilio_phone_number"

# Groq API key and endpoint
groq_api_key = "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"
groq_endpoint = "https://api.groq.com/v1/analyze"

# Route to handle incoming Twilio webhook requests
@app.route('/twilio-webhook', methods=['POST'])
def twilio_webhook():
    # Get the user's response from the Twilio request
    user_response = request.form.get('SpeechResult')

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

    try:
        # Make a request to Groq API to analyze user response
        response = requests.post(groq_endpoint, json=groq_payload, headers={"Authorization": f"Bearer {groq_api_key}"})
        response_data = response.json()

        # Get the intent detected by Groq
        intent = response_data['results']['analyze']['intents'][0]['name']

        # Process the intent
        if intent == "cumin_seeds_requirement":
            if user_response.lower() == "yes":
                # Provide a response based on user's requirement
                response_message = "Great! We have a variety of cumin seeds available. How many kilograms do you need?"
            elif user_response.lower() == "no":
                response_message = "No problem. If you have any other requirements, feel free to let us know."
            else:
                response_message = "Sorry, I didn't understand your response. Can you please say 'yes' or 'no'?"

    except Exception as e:
        print(f"Error analyzing user response: {e}")
        response_message = "Sorry, something went wrong while processing your request."

    # Respond with a message to Twilio
    twilio_response = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{response_message}</Say>
    </Response>
    """

    return twilio_response, 200

# Route to check if the Flask app is running
@app.route('/')
def check_flask_app():
    return 'Hello, Flask is running!'

if __name__ == '__main__':
    print("Flask app is running...")
    app.run(debug=True)
