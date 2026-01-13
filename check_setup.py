import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API key found.")
else:
    genai.configure(api_key=api_key)
    try:
        print("--- Available Models ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

print("\n--- Excel Headers ---")
try:
    df = pd.read_excel("data/d360hubspot.xlsx")
    print(list(df.columns))
    print("First row sample:", df.iloc[0].to_dict())
except Exception as e:
    print(f"Error reading Excel: {e}")
