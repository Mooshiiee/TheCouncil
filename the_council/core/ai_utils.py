from google.genai import types
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)

def analyze_fallacies_Old(text):
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
    
# Define the schema for each fallacy
class Fallacy(BaseModel):
    fallacy_type: str
    one_line_explanation: str

# Define the overall response schema
class FallacyAnalysis(BaseModel):
    found_fallacies: list[Fallacy]
    short_overall_suggestion: str

def analyze_fallacies(text_to_analyze):
    client = genai.Client(api_key=GEMINI_API_KEY)
    # The prompt that instructs the model what to do
    system_prompt = """
    You are a Logical Fallacy Analyzer designed to help forum users identify reasoning issues in their writing before posting.
    
    When analyzing text, identify potential logical fallacies including:
    - Ad hominem: Attacking the person rather than addressing their argument
    - Appeal to authority: Using an authority figure's opinion as definitive proof
    - Appeal to emotion: Using emotional appeals instead of logical reasoning
    - Appeal to popularity: Claiming something is true because many believe it
    - Bandwagon fallacy: Arguing that a position is correct because it's popular
    - Begging the question: Circular reasoning where the conclusion is assumed in the premise
    - Cherry-picking: Selectively using data that supports your argument
    - False analogy: Drawing comparison between things that aren't sufficiently similar
    - False cause (post hoc): Assuming that because B followed A, A caused B
    - False dichotomy: Presenting only two options when others exist
    - Hasty generalization: Drawing broad conclusions from insufficient evidence
    - Middle ground fallacy: Assuming the middle position between two extremes must be correct
    - No true Scotsman: Moving the goalposts to avoid counterexamples
    - Red herring: Introducing irrelevant information to distract from the main argument
    - Slippery slope: Claiming one small step will lead to extreme consequences
    - Straw man: Misrepresenting someone's argument to make it easier to attack
    - Tu quoque: Avoiding criticism by turning it back on the accuser
    
    Analyze the provided text thoroughly but concisely, focusing solely on the logical structure of arguments.
    Be specific about which parts of the text contain fallacies and why.
    If no fallacies are detected, provide a brief confirmation.
    """
    
    # Combine system prompt with text to analyze
    prompt = f"{system_prompt}\n\nAnalyze this text for logical fallacies: {text_to_analyze}"
    
    try:
        # Generate content with structured response
        response = client.models.generate_content(
            model='gemini-2.0-flash',  # Or the appropriate model version
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': FallacyAnalysis,
            },
        )
        # Return the parsed response
        result_dict = response.parsed.model_dump()
        return result_dict  
    
    except Exception as e:
        print(f"Error analyzing text: {e}")
        # Return a fallback response if an error occurs
        return FallacyAnalysis(
            found_fallacies=[],
            summary="Error analyzing the text.",
            overall_suggestion="Please try again with different text or contact support."
        )