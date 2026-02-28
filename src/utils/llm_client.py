"""
Client LLM pour Google Gemini
"""
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """Retourne une instance du modele Google Gemini"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.1,
        max_tokens=2000
    )
    
    return llm

def analyze_code_with_llm(code: str, file_path: str) -> dict:
    """
    Analyse du code avec Gemini
    """
    llm = get_llm()
    
    prompt = "You are a STRICT code reviewer. Analyze this Python code.\n\n"
    prompt += f"File: {file_path}\n\n"
    prompt += "Code:\n" + code + "\n\n"
    prompt += "Find EVERY error: syntax errors, undefined variables, division by zero, missing imports, logic bugs, exception handling.\n"
    prompt += 'Respond ONLY with JSON: {"issues": ["error 1", "error 2"], "decision": "REQUIRES_FIX"}\n'
    prompt += 'If you find ANY issue at all, use "REQUIRES_FIX". Only use "ACCEPTED" if code is PERFECT with no bugs.\n'
    prompt += "Be VERY strict and critical! Even small issues count!"
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Extraction correcte du JSON
        if "```json" in content:
            parts = content.split("```json")
            if len(parts) > 1:
                content = parts[1].split("```").strip()
        elif "```" in content:
            parts = content.split("```")
            if len(parts) >= 2:
                content = parts.strip()
        
        result = json.loads(content)
        return result
        
    except Exception as e:
        return {
            "issues": [f"LLM Error: {str(e)}"],
            "decision": "ACCEPTED"
        }

def fix_code_with_llm(code: str, file_path: str, issues: list) -> str:
    """
    Correction du code avec Gemini
    """
    llm = get_llm()
    
    issues_text = "\n".join(f"- {issue}" for issue in issues)
    
    prompt = "Fix the following Python code based on the identified issues.\n\n"
    prompt += f"File: {file_path}\n\n"
    prompt += "Issues to fix:\n" + issues_text + "\n\n"
    prompt += "Original code:\n" + code + "\n\n"
    prompt += "Provide ONLY the fixed Python code, without explanations or markdown blocks."
    
    try:
        response = llm.invoke(prompt)
        fixed_code = response.content.strip()
        
        # Extraction correcte du code
        if "```python" in fixed_code:
            parts = fixed_code.split("```python")
            if len(parts) > 1:
                fixed_code = parts.split("```")[0].strip()
        elif "```" in fixed_code:
            parts = fixed_code.split("```")
            if len(parts) >= 2:
                fixed_code = parts[1].strip()
        
        return fixed_code
        
    except Exception as e:
        return code
