import os
import pandas as pd

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class JobRetrievalAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )

        self.persist_directory = "database"

        self.vector_store = None


    def load_jobs(self):

        jobs_df = pd.read_csv("data/jobs.csv")

        documents = []
        ids = []

        for _, row in jobs_df.iterrows():

            job_text = f"""
Job Title: {row['job_title']}

Company: {row['company']}

Skills Required: {row['skills']}

Experience Required: {row['experience']}

Location: {row['location']}

Job Description:
{row['description']}
"""

            document = Document(
                page_content=job_text,
                metadata={
                    "job_id": str(row["job_id"]),
                    "job_title": row["job_title"],
                    "company": row["company"],
                    "location": row["location"]
                }
            )

            documents.append(document)
            ids.append(str(row["job_id"]))

        return documents, ids


    def create_vector_store(self):

        self.vector_store = Chroma(
            collection_name="jobs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        documents, ids = self.load_jobs()

        # Add documents to ChromaDB
        self.vector_store.add_documents(
            documents=documents,
            ids=ids
        )


    def retrieve_jobs(self, candidate_profile, k=3):

        if self.vector_store is None:
            self.create_vector_store()

        # IMPORTANT:
        # Ensure candidate profile is plain text
        if not isinstance(candidate_profile, str):
            candidate_profile = str(candidate_profile)

        results = self.vector_store.similarity_search(
            query=candidate_profile,
            k=k
        )

        return results