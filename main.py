import os
import streamlit as st
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# API endpoint for the Gemini model
API_URL = os.getenv("API_URL")

# Function to call the Gemini API

def generate_gemini_content(prompt):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    # Send the POST request
    response = requests.post(f"{API_URL}?key={GOOGLE_API_KEY}", headers=headers, json=data)

    # Log full response for debugging
    if response.status_code == 200:
        try:
            # Access the 'candidates' field
            response_data = response.json()
           # st.write("Full API Response: ", response_data)  # Display the full response in Streamlit for debugging

            # Get the text from the first candidate in the response
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except KeyError as e:
            return f"KeyError: {e}. Response Data: {response.json()}"
    else:
        return f"Error: {response.status_code}, {response.text}"


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

# Display the chatbot's title on the page
st.title("🤖 ChatBot - Pro")

# Display the chat history
for message in st.session_state.chat_session:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    
    # Call Gemini API for response
    gemini_response = generate_gemini_content(user_prompt)
    
    # Display Gemini-Pro's response
    st.chat_message("assistant").markdown(gemini_response)
    
    # Save the conversation in session state
    st.session_state.chat_session.append({"role": "user", "text": user_prompt})
    st.session_state.chat_session.append({"role": "assistant", "text": gemini_response})
