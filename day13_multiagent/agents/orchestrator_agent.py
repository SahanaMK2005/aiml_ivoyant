from agents.teacher_agent import TeacherAgent
from agents.quiz_agent import QuizAgent


class OrchestratorAgent:

    def __init__(self):

        self.teacher_agent = TeacherAgent()
        self.quiz_agent = QuizAgent()

    def process_topic(self, topic):

        # Teacher Agent generates explanation
        explanation = self.teacher_agent.explain_topic(topic)

        # Quiz Agent generates quiz
        quiz = self.quiz_agent.generate_quiz(topic)

        # Combine responses
        return {
            "topic": topic,
            "explanation": explanation,
            "quiz": quiz
        }