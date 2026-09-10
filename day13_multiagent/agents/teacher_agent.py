import os
from google import genai


class TeacherAgent:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key)

    def explain_topic(self, topic):

        prompt = f"""
        You are a helpful AI teacher.

        Explain the topic "{topic}" in simple language.

        Include:
        1. Definition
        2. Simple explanation
        3. One real-world example

        Keep the response clear and beginner-friendly.
        """

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text