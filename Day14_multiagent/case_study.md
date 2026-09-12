# Day 14 – Multi-Agent Systems Case Studies

## Use Case 1: Multi-Agent Recruitment System

### Description

A company receives many resumes and wants to find the **best candidate for a job**.

Different agents perform different tasks:

- **Resume Screening Agent** → Reads the resume.
- **Skill Matching Agent** → Matches candidate skills with job requirements.
- **Candidate Evaluation Agent** → Evaluates the candidate.
- **Ranking Agent** → Ranks the candidates.

### Flow

```text
Job Requirements + Candidate Resumes
                ↓
      Resume Screening Agent
                ↓
       Candidate Information
                ↓
       Skill Matching Agent
                ↓
         Skill Match Result
                ↓
    Candidate Evaluation Agent
                ↓
        Candidate Ranking
                ↓
     Shortlisted Candidates