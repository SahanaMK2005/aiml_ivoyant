import os

from langchain_google_genai import ChatGoogleGenerativeAI


class RankingAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=api_key
        )

    def rank_jobs(self, candidate_profile, jobs):

        jobs_text = ""

        for index, job in enumerate(jobs, start=1):

            jobs_text += f"""
JOB {index}

Job Title: {job.metadata.get('job_title')}

Company: {job.metadata.get('company')}

Location: {job.metadata.get('location')}

Job Details:
{job.page_content}

"""

        prompt = f"""
You are a Ranking and Explanation Agent in an AI-powered
Job Recommendation System.

Your task is to analyze the candidate profile and the retrieved jobs.

Compare the candidate with each job based on:

1. Technical skills
2. Preferred role
3. Experience
4. Overall relevance

Then rank the jobs from BEST MATCH to LOWEST MATCH.

For each job, provide:

- Rank
- Job Title
- Company
- Match Score out of 100
- Why the job matches the candidate
- Missing or weaker skills, if any

Candidate Profile:

{candidate_profile}


Retrieved Jobs:

{jobs_text}


Important instructions:

- Rank only the jobs provided.
- Do not create new jobs.
- Do not invent candidate skills.
- Give a realistic match score.
- Clearly explain the ranking.
"""

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])

            return "\n".join(text_parts)

        return str(content)