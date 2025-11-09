from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

print("Using model:", MODEL_NAME)
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content("Hello, how are you?")
    print("✅ Gemini response:", response.text.strip() if hasattr(response, "text") else response)
except Exception as e:
    print("❌ Error while generating:", e)
