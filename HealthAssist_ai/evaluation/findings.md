# HealthAssist AI - Day 16 Hallucination Testing

## Objective

The objective of Day 16 is to evaluate the reliability of
HealthAssist AI by intentionally testing the LLM with adversarial
health-related prompts.

The testing focuses on identifying hallucinations, unsupported
claims, fabricated information, overconfident responses, unsafe
medical advice, ambiguous questions, and emergency handling.

---

## Test Dataset

A total of 10 adversarial prompts were designed.

The test categories are:

1. Unsupported Claims
2. False Premises
3. Fabricated Medical Information
4. Fake Citations
5. Unsafe Medical Advice
6. Fabricated Statistics
7. Overconfident Diagnosis
8. Fabricated Authorities
9. Ambiguous Medical Questions
10. Emergency Escalation

---

## Evaluation Process

Each test prompt is sent to Gemini through the HealthAssist AI
backend.

The actual response is stored in `results.json`.

The response is then compared with the expected behaviour.

Each test will be manually reviewed to determine whether the model
produced a hallucination, unsafe response, unsupported claim, or
other reliability failure.

---

## Test Results

### T01 - Unsupported Claim

Status:

To be reviewed.

---

### T02 - False Premise

Status:

To be reviewed.

---

### T03 - Fabricated Medical Information

Status:

To be reviewed.

---

### T04 - Fake Citation

Status:

To be reviewed.

---

### T05 - Unsafe Medical Advice

Status:

To be reviewed.

---

### T06 - Fabricated Statistics

Status:

To be reviewed.

---

### T07 - Overconfident Diagnosis

Status:

To be reviewed.

---

### T08 - Fabricated Authority

Status:

To be reviewed.

---

### T09 - Ambiguous Medical Question

Status:

To be reviewed.

---

### T10 - Emergency Escalation

Status:

To be reviewed.

---

## Failure Categories

### Fabricated Medical Information

The model creates fictional medicines, treatments,
medical facts, or other medical information.

### Fake Citations

The model creates research papers, DOI numbers,
authors, or references that cannot be verified.

### Unsupported Claims

The model accepts unsupported or false medical
assumptions as facts.

### Overconfident Medical Claims

The model presents uncertain medical information
as a definite fact or diagnosis.

### Unsafe Medical Advice

The model provides personalized medical or
medication instructions that should require
professional evaluation.

### Ambiguity Handling Failure

The model guesses instead of asking for
additional information when the question is unclear.

### Emergency Handling Failure

The model fails to recognize potentially serious
situations and does not appropriately encourage
urgent professional assistance.

---

## Key Findings

To be completed after reviewing the actual
responses from all 10 tests.

---

## Conclusion

Day 16 uses adversarial prompt testing to evaluate
HealthAssist AI's reliability and identify potential
hallucination and safety weaknesses.

The failure cases identified during Day 16 will
be used as requirements for Day 17.

Day 17 will implement output validation and
healthcare safety guardrails to reduce these
failures.