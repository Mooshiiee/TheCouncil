from google.genai import types
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)

def analyze_fallacies(text):
    """Analyze text for logical fallacies using Google GenAI"""
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""Analyze this text for logical fallacies. 
    Return a concise bullet point list of any found fallacies with brief explanations.
    If no fallacies are found, return 'No detectable fallacies found'.
    Text"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=prompt),
            contents=text
        )
                        
        return response.text
    except Exception as e:
        return f"Analysis error: {str(e)}"
