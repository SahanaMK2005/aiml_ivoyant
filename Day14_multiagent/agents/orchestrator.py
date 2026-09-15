from agents.profile_extraction_agent import ProfileExtractionAgent
from agents.job_retrieval_agent import JobRetrievalAgent
from agents.ranking_agent import RankingAgent
from agents.candidate_storage import CandidateStorage


class OrchestratorAgent:

    def __init__(self):

        # Initialize agents
        self.profile_agent = ProfileExtractionAgent()

        self.retrieval_agent = JobRetrievalAgent()

        self.ranking_agent = RankingAgent()

        # Initialize candidate storage
        self.candidate_storage = CandidateStorage()


    def run(self, resume_path):

        # =====================================
        # AGENT 1: PROFILE EXTRACTION
        # =====================================

        print("\n===== PROFILE EXTRACTION AGENT =====")

        candidate_profile = self.profile_agent.extract_profile(
            resume_path
        )

        candidate_profile = str(candidate_profile)

        print(candidate_profile)


        # =====================================
        # STORE CANDIDATE INFORMATION
        # =====================================

        self.candidate_storage.save_candidate(
            resume_name=resume_path,
            candidate_profile=candidate_profile
        )


        # =====================================
        # AGENT 2: JOB RETRIEVAL
        # =====================================

        print("\n===== JOB RETRIEVAL AGENT =====")

        matching_jobs = self.retrieval_agent.retrieve_jobs(
            candidate_profile,
            k=3
        )

        for index, job in enumerate(matching_jobs, start=1):

            print(f"\n{index}. {job.metadata['job_title']}")
            print(f"Company: {job.metadata['company']}")
            print(f"Location: {job.metadata['location']}")


        # =====================================
        # AGENT 3: RANKING
        # =====================================

        print("\n===== RANKING & EXPLANATION AGENT =====")

        ranked_jobs = self.ranking_agent.rank_jobs(
            candidate_profile,
            matching_jobs
        )


        return {
            "candidate_profile": candidate_profile,
            "matching_jobs": matching_jobs,
            "ranked_jobs": ranked_jobs
        }