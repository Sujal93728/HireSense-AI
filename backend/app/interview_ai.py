import random

QUESTIONS = {
    "Software Engineer": [
        "What is Object-Oriented Programming?",
        "Explain the difference between a list and a tuple in Python.",
        "What is polymorphism?",
        "What are REST APIs?",
        "Explain multithreading in Python."
    ],

    "Frontend Developer": [
        "What is the Virtual DOM?",
        "Explain React Hooks.",
        "Difference between var, let and const.",
        "What is state management?",
        "Explain CSS Flexbox."
    ],

    "Backend Developer": [
        "What is FastAPI?",
        "Explain JWT Authentication.",
        "Difference between SQL and NoSQL.",
        "What is ORM?",
        "Explain database indexing."
    ],

    "Data Scientist": [
        "What is Machine Learning?",
        "Difference between supervised and unsupervised learning.",
        "Explain overfitting.",
        "What is feature engineering?",
        "Difference between regression and classification."
    ]
}


def generate_interview_question(role: str, difficulty: str):
    """
    Returns one interview question based on role.
    """

    questions = QUESTIONS.get(
        role,
        QUESTIONS["Software Engineer"]
    )

    return random.choice(questions)


def evaluate_answer(question: str, answer: str):
    """
    Very simple AI evaluator.
    """

    word_count = len(answer.split())

    if word_count > 80:
        score = 10
    elif word_count > 60:
        score = 9
    elif word_count > 40:
        score = 8
    elif word_count > 25:
        score = 7
    elif word_count > 10:
        score = 6
    else:
        score = 4

    strengths = [
        "Clear explanation",
        "Relevant answer"
    ]

    weaknesses = []

    if word_count < 20:
        weaknesses.append("Answer is too short")

    suggestions = [
        "Include practical examples",
        "Explain concepts in more detail"
    ]

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }