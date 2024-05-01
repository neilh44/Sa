from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define route for receiving user responses during the call
@app.route("/twilio/inbound_call", methods=["POST"])
def inbound_call():
    # Get user response from Twilio request
    user_response = request.form["SpeechResult"]
    
    # Analyze user response using spaCy
    doc = nlp(user_response)
    
    # Process analysis results
    # For demonstration, let's just return the entities found in the user response
    entities = [ent.text for ent in doc.ents]
    
    # Prepare response
    response = {
        "user_response": user_response,
        "entities": entities
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
