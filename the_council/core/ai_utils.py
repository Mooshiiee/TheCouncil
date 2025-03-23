from django.conf import settings
import google.generativeai as genai

genai.configure(api_key=settings.GENAI_API_KEY)

def analyze_fallacies(text):
    """Analyze text for logical fallacies using Google GenAI"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""Analyze this text for logical fallacies. 
    Return a concise bullet point list of any found fallacies with brief explanations.
    If no fallacies are found, return 'No detectable fallacies found'.
    Text: {text}"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analysis error: {str(e)}"
