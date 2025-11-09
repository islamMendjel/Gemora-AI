import os
from dotenv import load_dotenv
import google.generativeai as genai

# Always load .env before configuring the API
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

def get_gemini_response(prompt: str) -> str:
    """
    Generate a Gemini response for a given prompt.
    Returns safe text output even if API fails.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        # Clean extraction of text
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()

        return "⚠️ AI response was empty."

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return f"AI Error: {str(e)}"
