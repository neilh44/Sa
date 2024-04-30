from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/handle-response', methods=['POST'])
def handle_response():
    # Parse the Twilio Voice Request
    call_sid = request.form.get('CallSid')
    user_response = request.form.get('SpeechResult')

    # Process user response (replace this with your logic)
    if user_response:
        # Handle user response based on your application's logic
        print("User response:", user_response)
        # Respond with TwiML
        twiml_response = VoiceResponse()
        twiml_response.say("Thank you for your response. Goodbye!")
        return str(twiml_response), 200
    else:
        # If no response received, prompt user again
        twiml_response = VoiceResponse()
        twiml_response.say("Sorry, I didn't catch that. Please respond with yes or no.")
        return str(twiml_response), 200

if __name__ == '__main__':
    app.run(debug=True)
  
