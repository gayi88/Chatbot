import os
import google.generativeai as genai
from dotenv import load_dotenv

# Using Google Generative AI API
# Loading environment variables from .env file

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

#Gemini model initialization
#using the latest Gemini model gemini-1.5-pro

model = genai.GenerativeModel("gemini-1.5-pro")

# Function to ask Gemini model a question with context
def ask_gemini(context, question):
    prompt = f"""Use the following text as context and answer the question in English, even if the input is in Swedish:

CONTEXT:
{context}

QUESTION:
{question}
"""
# call the Gemini model to generate content based on the prompt
    response = model.generate_content(prompt)

#return the generated answer
    return response.text.strip()
