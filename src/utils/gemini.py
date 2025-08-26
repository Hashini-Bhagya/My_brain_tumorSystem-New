import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_tumor_info_from_gemini(tumor_type):
    """Get information about a tumor type from Gemini AI"""
    if not GEMINI_API_KEY:
        return "Gemini API not configured. Please add GEMINI_API_KEY to your environment variables."
    
    # Create the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config=generation_config
    )
    
    # Create prompt based on tumor type
    if tumor_type == 'notumor':
        prompt = """Please provide a concise, medically accurate explanation about what it means when 
        a brain MRI shows no tumor. Include information about the reliability of the test and 
        recommendations for follow-up care. Format your response in Markdown."""
    else:
        prompt = f"""Please provide a concise, medically accurate explanation about {tumor_type} brain tumors. 
        Include information about symptoms, causes, treatment options, and prognosis. 
        Format your response in Markdown."""
    
    # Generate content
    response = model.generate_content(prompt)
    
    return response.text