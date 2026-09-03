import os
import json
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def analyze_contract(text: str) -> dict:
    """Analyzes contract text using Gemini and returns structured JSON."""
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""
    Analyze the following contract and extract key information. 
    Return the analysis strictly as a JSON object with the following keys:
    - "parties": List of parties involved
    - "effective_date": The effective date of the contract
    - "clauses": A list of important clauses
    - "risks": A list of potential risks or liabilities

    Contract Text:
    {text}
    """
    
    response = model.generate_content(prompt)
    try:
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Gemini response as JSON: {e}\nResponse text: {response.text}")
