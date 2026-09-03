import os 
from google import genai 
from dotenv import load_dotenv 
 
# Loading environment variables from .env file 
load_dotenv() 
 
GENAI_API_KEY = os.getenv("GENAI_API_KEY") 
 
# Gemini client 
client = genai.Client(api_key=GENAI_API_KEY) 
 
# Gemini model 
model = "gemini-2.5-flash" 
 
 
# Function to ask Gemini model a question with context 
def ask_gemini(context, question): 
 
    prompt = f"""Use the following text as context and answer the question in English, even if the input is in Swedish: 
 
CONTEXT: 
{context} 
 
QUESTION: 
{question} 
""" 
 
    # Generate response 
    response = client.models.generate_content( 
        model=model, 
        contents=prompt 
    ) 
 
    # Return generated answer 
    return response.text.strip()