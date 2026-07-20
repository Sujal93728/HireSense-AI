import random

QUESTION_BANK = {
    "python": [
        "Explain Python decorators.",
        "What is the difference between a list and a tuple?",
        "Explain generators in Python.",
        "What are Python context managers?",
        "What is the GIL?"
    ],

    "react": [
        "What are React Hooks?",
        "Explain the Virtual DOM.",
        "Difference between State and Props.",
        "What is useEffect?",
        "What is Context API?"
    ],

    "javascript": [
        "Explain closures.",
        "Difference between var, let and const.",
        "Explain promises.",
        "What is async/await?",
        "Explain event bubbling."
    ],

    "sql": [
        "Difference between DELETE and TRUNCATE.",
        "Explain INNER JOIN.",
        "Write a query to find duplicate rows.",
        "What is normalization?",
        "Difference between WHERE and HAVING."
    ],

    "machine learning": [
        "Difference between supervised and unsupervised learning.",
        "Explain overfitting.",
        "What is cross validation?",
        "Explain gradient descent.",
        "What is Random Forest?"
    ],

    "docker": [
        "Difference between Docker and Virtual Machines.",
        "What is Docker Compose?",
        "Explain Docker volumes.",
        "What are Docker images?",
        "Explain Docker networking."
    ]
}


def generate_questions(description: str):
    description = (description or "").lower()

    questions = []

    for skill, skill_questions in QUESTION_BANK.items():
        if skill in description:
            questions.extend(random.sample(skill_questions, min(3, len(skill_questions))))

    if not questions:
        questions = [
            "Tell me about yourself.",
            "Why do you want this role?",
            "Describe a challenging project.",
            "Explain your strengths.",
            "Describe a difficult bug you fixed."
        ]

    return questions[:10]