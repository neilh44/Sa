import asyncio
import websockets
from groq import Groq

# Set your Groq API key
api_key = "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"

# Initialize the Groq client
groq_client = Groq(api_key=api_key)

# Function to generate response using Groq's chat completion
def generate_response(message):
    try:
        # Create a chat completion with the user's message
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": message}
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=150,
            top_p=0.9,
            stop=None,
            stream=False,
        )

        # Return the content of the first choice
        return completion.choices[0].message.content
    except Exception as e:
        return f"Chat Completion Error: {e}"

# Handle incoming connections
async def handle_connection(websocket, path):
    async for message in websocket:
        # Generate response based on user's message
        response = generate_response(message)
        
        # Send the response back to the client
        await websocket.send(response)

# Start the WebSocket server
async def start_server():
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print(f"Server started at ws://{server.sockets[0].getsockname()[0]}:{server.sockets[0].getsockname()[1]}")
    await server.wait_closed()

# Run the event loop to start the server
asyncio.run(start_server())
