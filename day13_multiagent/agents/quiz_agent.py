import os
import json
from google import genai


class QuizAgent:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key)

    def generate_quiz(self, topic):

        prompt = f"""
You are an AI quiz generator.

Create exactly 3 beginner-friendly multiple-choice questions about "{topic}".

Return ONLY valid JSON.

Use this exact format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": "Correct option text"
    }}
]

Rules:
- Create exactly 3 questions.
- Each question must have exactly 4 options.
- Only one option must be correct.
- The correct_answer must exactly match one of the options.
- Do not include explanations.
- Do not include markdown.
- Do not write ```json.
- Return only the JSON array.
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        quiz_text = response.text

        return json.loads(quiz_text)