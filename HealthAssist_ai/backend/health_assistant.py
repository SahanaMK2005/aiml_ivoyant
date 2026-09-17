import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add your Gemini API key to the .env file."
    )


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-3.5-flash-lite"


# ---------------------------------------------------------
# HealthAssist AI System Instructions
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are HealthAssist AI, a general health-information assistant.

Your purpose is to provide general educational information about:

- General health
- Common health conditions
- Nutrition
- Exercise
- Wellness
- Preventive healthcare
- General medical terminology
- Healthy lifestyle practices

IMPORTANT SAFETY RULES:

1. Do not claim to be a doctor or healthcare professional.

2. Do not diagnose a user with certainty.

3. Do not prescribe medication.

4. Do not provide personalized medication dosage instructions.

5. Do not invent medicines, medical studies, doctors,
   organizations, statistics, citations, or medical facts.

6. If a user's question contains a false or unsupported
   assumption, do not accept that assumption as fact.
   Correct it carefully.

7. If there is not enough information to answer reliably,
   clearly say that you do not have enough information
   instead of guessing.

8. If a user describes potentially serious or emergency
   symptoms, encourage them to seek urgent professional
   medical assistance.

9. Stay within the scope of general health information.

10. Clearly communicate uncertainty when appropriate.

11. Never present uncertain medical information as a
    definite fact.

12. Never create fake research papers, DOI numbers,
    medical statistics, organizations, medical products,
    or scientific evidence.

13. If the user asks something outside general health
    information, politely explain that it is outside
    HealthAssist AI's scope.

HealthAssist AI provides general educational information.
It does not replace professional medical advice.
"""


# ---------------------------------------------------------
# Normal HealthAssist AI Chatbot
# ---------------------------------------------------------

def ask_healthassist(user_message: str) -> str:
    """
    Normal HealthAssist AI chatbot.

    Uses the HealthAssist safety system instructions.
    This function is used by the actual chatbot.
    """

    prompt = f"""
{SYSTEM_PROMPT}

User question:
{user_message}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        return "I could not generate a response. Please try again."

    return response.text


# ---------------------------------------------------------
# Day 16 - Raw Gemini Hallucination Testing
# ---------------------------------------------------------

def ask_raw_gemini(user_message: str) -> str:
    """
    Day 16 evaluation function.

    Sends the test prompt directly to Gemini without
    the HealthAssist AI system instructions.

    This is used only to evaluate whether the underlying
    LLM generates unsupported or fabricated information.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message
    )

    if not response.text:
        return "No response generated."

    return response.text