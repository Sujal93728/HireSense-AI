TECH_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "React",
    "Node.js",
    "FastAPI",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "MongoDB",
    "PostgreSQL",
    "Redis",
    "Machine Learning",
    "TensorFlow",
    "PyTorch",
    "JavaScript",
    "TypeScript",
]


def analyze_resume(resume_text: str):
    text = resume_text.lower()

    found_skills = []

    for skill in TECH_SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = [
        skill
        for skill in TECH_SKILLS
        if skill not in found_skills
    ]

    score = int((len(found_skills) / len(TECH_SKILLS)) * 100)

    suggestions = []

    if "docker" not in text:
        suggestions.append("Learn Docker for containerization.")

    if "aws" not in text:
        suggestions.append("Gain experience with AWS cloud services.")

    if "sql" not in text:
        suggestions.append("Improve SQL and database skills.")

    if "react" not in text:
        suggestions.append("Build at least one React project.")

    return {
        "score": score,
        "skills": found_skills,
        "missing_skills": missing_skills[:10],
        "suggestions": suggestions,
    }