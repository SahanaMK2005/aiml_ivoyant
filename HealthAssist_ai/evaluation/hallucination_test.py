import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.health_assistant import ask_raw_gemini


BASE_DIR = Path(__file__).resolve().parent
PROMPTS_FILE = BASE_DIR / "prompts.json"
RESULTS_FILE = BASE_DIR / "results.json"


def load_test_prompts():
    with open(PROMPTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def run_tests():
    test_prompts = load_test_prompts()
    results = []

    print()
    print("=" * 70)
    print("HealthAssist AI - Day 16 Hallucination Testing")
    print("=" * 70)

    print(f"\nTotal tests: {len(test_prompts)}")

    for test in test_prompts:

        print()
        print("-" * 70)
        print(f"Test ID: {test['id']}")
        print(f"Category: {test['category']}")
        print(f"Prompt: {test['prompt']}")

        print("\nSending prompt to Gemini...")

        try:
            response = ask_raw_gemini(test["prompt"])

            # ---------------------------------------------------------
            # Show only a short response preview in the terminal
            # ---------------------------------------------------------
            preview = response.replace("\n", " ")

            if len(preview) > 250:
                preview = preview[:250] + "..."

            print("\nAI Response Preview:")
            print(preview)

            # ---------------------------------------------------------
            # Save the COMPLETE response for evaluation
            # ---------------------------------------------------------
            result = {
                "id": test["id"],
                "category": test["category"],
                "prompt": test["prompt"],
                "expected_behavior": test["expected_behavior"],
                "actual_response": response,
                "failure_detected": None,
                "failure_explanation": "",
                "review_status": "Needs manual review"
            }

        except Exception as error:

            print("\nERROR:")
            print(error)

            result = {
                "id": test["id"],
                "category": test["category"],
                "prompt": test["prompt"],
                "expected_behavior": test["expected_behavior"],
                "actual_response": None,
                "failure_detected": None,
                "failure_explanation": str(error),
                "review_status": "API Error"
            }

        results.append(result)

    # -------------------------------------------------------------
    # Save all test results
    # -------------------------------------------------------------
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("=" * 70)

    print(f"Tests executed: {len(results)}")
    print(f"Results saved to: {RESULTS_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()