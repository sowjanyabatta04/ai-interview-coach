import warnings
warnings.filterwarnings("ignore")

import google.generativeai as genai

API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

def get_ai_feedback(question, answer):
    prompt = f"""
You are an interview coach.

Question: {question}
Candidate Answer: {answer}

Give short feedback in this format:
Score: X/10
Strong point: one line
Missing point: one line
Suggestion: one line
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
Score: N/A
Strong point: Answer received.
Missing point: AI server unavailable / quota exceeded.
Suggestion: Try again later.
"""