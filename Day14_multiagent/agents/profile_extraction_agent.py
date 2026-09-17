import os
from pathlib import Path

from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI


class ProfileExtractionAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=api_key
        )


    def read_resume(self, resume_path):

        file_extension = Path(resume_path).suffix.lower()

        # TXT FILE
        if file_extension == ".txt":

            return Path(resume_path).read_text(
                encoding="utf-8"
            )


        # PDF FILE
        elif file_extension == ".pdf":

            reader = PdfReader(resume_path)

            resume_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    resume_text += text + "\n"

            return resume_text


        else:

            raise ValueError(
                "Only TXT and PDF files are supported."
            )


    def extract_profile(self, resume_path):

        resume_text = self.read_resume(resume_path)

        prompt = f"""
You are a Profile Extraction Agent in an AI-powered
Job Recommendation System.

Analyze the candidate's resume and extract:

1. Name
2. Technical Skills
3. Experience
4. Education
5. Preferred Role

Resume:
{resume_text}

Provide the information clearly.
Do not add information that is not present in the resume.
"""

        response = self.llm.invoke(prompt)

        # Extract clean text from Gemini response
        if isinstance(response.content, list):

            profile_text = ""

            for item in response.content:

                if isinstance(item, dict) and "text" in item:
                    profile_text += item["text"]

                else:
                    profile_text += str(item)

            return profile_text

        return str(response.content)