import pandas as pd
import os

def load_profile(file_path):
    """Reads the company profile from a text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile file not found: {file_path}")
    if file_path.lower().endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def load_leads(file_path):
    """Reads leads from a CSV or Excel file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Leads file not found: {file_path}")
    
    if file_path.lower().endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.lower().endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
