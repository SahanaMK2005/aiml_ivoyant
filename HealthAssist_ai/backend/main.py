from pathlib import Path
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.health_assistant import ask_healthassist, ask_raw_gemini


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"

EVALUATION_DIR = BASE_DIR / "evaluation"

PROMPTS_FILE = EVALUATION_DIR / "prompts.json"


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="HealthAssist AI API",
    description="Health Information and Safety Chatbot API",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# STATIC FRONTEND
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


# =====================================================
# REQUEST / RESPONSE MODELS
# =====================================================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class EvaluationRequest(BaseModel):
    test_id: str


# =====================================================
# LOAD EVALUATION PROMPTS
# =====================================================

def load_evaluation_tests():

    with open(
        PROMPTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =====================================================
# HOME PAGE
# =====================================================

@app.get("/")
def root():

    return FileResponse(
        str(FRONTEND_DIR / "index.html")
    )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "application": "HealthAssist AI"
    }


# =====================================================
# NORMAL CHAT
# =====================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    response = ask_healthassist(
        request.message
    )

    return {
        "response": response
    }


# =====================================================
# DAY 16 - GET ALL TEST CASES
# =====================================================

@app.get("/evaluation/tests")
def get_evaluation_tests():

    tests = load_evaluation_tests()

    return {
        "tests": [
            {
                "id": test["id"],
                "category": test["category"]
            }
            for test in tests
        ]
    }


# =====================================================
# DAY 16 - GET ONE TEST CASE
# =====================================================

@app.get("/evaluation/test/{test_id}")
def get_evaluation_test(test_id: str):

    tests = load_evaluation_tests()

    for test in tests:

        if test["id"] == test_id:

            return test

    raise HTTPException(
        status_code=404,
        detail="Test case not found."
    )


# =====================================================
# DAY 16 - RUN ONE HALLUCINATION TEST
# =====================================================

@app.post("/evaluation/run")
def run_evaluation(
    request: EvaluationRequest
):

    tests = load_evaluation_tests()

    selected_test = None

    for test in tests:

        if test["id"] == request.test_id:

            selected_test = test

            break


    if selected_test is None:

        raise HTTPException(
            status_code=404,
            detail="Test case not found."
        )


    # -------------------------------------------------
    # Send prompt directly to raw Gemini
    # -------------------------------------------------

    actual_response = ask_raw_gemini(
        selected_test["prompt"]
    )


    # -------------------------------------------------
    # Day 16 requires manual evaluation.
    # We do NOT automatically claim hallucination.
    # -------------------------------------------------

    return {

        "id": selected_test["id"],

        "category": selected_test["category"],

        "prompt": selected_test["prompt"],

        "expected_behavior":
            selected_test["expected_behavior"],

        "actual_response":
            actual_response,

        "result":
            "Needs Manual Review",

        "failure_detected":
            False,

        "failure_type":
            "",

        "failure_explanation":
            "Review the actual response against the expected behavior.",

        "summary": {

            "passed": 0,

            "failed": 0,

            "hallucinations": 0

        }

    }