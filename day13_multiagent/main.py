from agents.orchestrator_agent import OrchestratorAgent


def main():

    topic = "RAG"

    orchestrator = OrchestratorAgent()

    result = orchestrator.process_topic(topic)

    print(f"\n📖 TOPIC: {result['topic']}")

    print("\n📚 EXPLANATION:\n")
    print(result["explanation"])

    print("\n📝 QUIZ:\n")
    print(result["quiz"])


if __name__ == "__main__":
    main()