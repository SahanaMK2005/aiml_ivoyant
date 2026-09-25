# AI-Powered Multi-Agent Job Recommendation System

## Project Overview

The AI-Powered Multi-Agent Job Recommendation System helps candidates find suitable jobs based on their resume.

The user can upload a resume in **PDF or TXT format**. The system extracts candidate information, retrieves relevant jobs, ranks them, and provides job recommendations.

The project uses a **Multi-Agent Architecture**, where different agents perform specialized tasks. An **Orchestrator Agent** manages the complete workflow.

---

## Features

- Upload Resume in PDF or TXT format
- Extract candidate information from the resume
- Store candidate information in SQLite database
- Retrieve relevant jobs using ChromaDB
- Generate embeddings for job data
- Perform similarity search
- Retrieve Top-K matching jobs
- Rank jobs based on candidate profile
- Provide explanations for job recommendations
- Streamlit User Interface

---

# Multi-Agent Architecture

The system uses three specialized agents and one Orchestrator Agent.

## Agents

### 1. Profile Extraction Agent

This agent reads the uploaded resume and extracts:

- Name
- Technical Skills
- Experience
- Education
- Preferred Role

Gemini LLM is used to extract the candidate profile.

---

### 2. Job Retrieval Agent

This agent retrieves relevant jobs based on the candidate profile.

It uses:

- Embeddings
- ChromaDB
- Similarity Search
- Top-K Retrieval

The job data is converted into embeddings and stored in ChromaDB.

---

### 3. Ranking Agent

This agent analyzes the candidate profile and retrieved jobs.

It:

- Compares candidate skills with job requirements
- Evaluates job suitability
- Ranks the jobs
- Generates match scores
- Explains why each job matches the candidate

---

### 4. Orchestrator Agent

The Orchestrator Agent manages the communication between all agents.

It controls the complete workflow:

```text
Profile Extraction Agent
        ↓
Job Retrieval Agent
        ↓
Ranking Agent
        ↓
Final Job Recommendations

python -m streamlit run app.py