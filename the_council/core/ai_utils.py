from django.conf import settings
import google as genai
from google.generativeai import types



def analyze_fallacies(text):
    """Analyze text for logical fallacies using Google GenAI"""
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    prompt = f"""Analyze this text for logical fallacies. 
    Return a concise bullet point list of any found fallacies with brief explanations.
    If no fallacies are found, return 'No detectable fallacies found'.
    Text"""
    
    try:
        response = model.generate_content(prompt)
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=prompt),
            contents=text
        )
                        
        return response.text
    except Exception as e:
        return f"Analysis error: {str(e)}"
