# Assistant AI Chatbot

A conversational AI chatbot built with Python, Streamlit, and Groq API.

## Features
- AI-powered question answering
- Bengali and English support
- Interactive Streamlit interface

## Tech Stack
- Python
- Streamlit
- Groq API

## Local Setup

Install dependencies:

    python -m pip install -r requirements.txt

Create a local .env file with your Groq API key:

    GROQ_API_KEY=your_groq_api_key_here
    GROQ_MODEL=openai/gpt-oss-20b

Never upload your real .env file or API key to GitHub.

## Run the App

    streamlit run app.py

## Deployment

Deploy with Streamlit Community Cloud. Add your API key under App Settings > Secrets.
