import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model_list = genai.list_models()
for m in model_list:
    print(f"Name: {m.name}, Methods: {m.supported_generation_methods}")
