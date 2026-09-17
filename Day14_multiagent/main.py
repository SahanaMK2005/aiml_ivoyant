from agents.orchestrator import OrchestratorAgent


def main():

    orchestrator = OrchestratorAgent()

    result = orchestrator.run(
        "data/sample_resume.txt"
    )

    print("\n===== FINAL JOB RECOMMENDATIONS =====\n")

    print(result["ranked_jobs"])


if __name__ == "__main__":
    main()