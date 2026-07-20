ROADMAP = {
    "Python": {"level": "Beginner", "days": 7},
    "Java": {"level": "Intermediate", "days": 10},
    "JavaScript": {"level": "Beginner", "days": 7},
    "React": {"level": "Intermediate", "days": 10},
    "SQL": {"level": "Intermediate", "days": 5},
    "Docker": {"level": "Intermediate", "days": 7},
    "Kubernetes": {"level": "Advanced", "days": 14},
    "AWS": {"level": "Intermediate", "days": 14},
    "Fastapi": {"level": "Intermediate", "days": 5},
    "Machine Learning": {"level": "Advanced", "days": 20},
    "Tensorflow": {"level": "Advanced", "days": 15},
    "Git": {"level": "Beginner", "days": 3},
    "Github": {"level": "Beginner", "days": 2},
    "HTML": {"level": "Beginner", "days": 3},
    "CSS": {"level": "Beginner", "days": 3},
    "Tailwind": {"level": "Beginner", "days": 4},
    "Bootstrap": {"level": "Beginner", "days": 3},
    "Node": {"level": "Intermediate", "days": 8},
    "Express": {"level": "Intermediate", "days": 5},
    "Flask": {"level": "Beginner", "days": 4},
    "Django": {"level": "Intermediate", "days": 8},
}


def generate_roadmap(missing_skills):
    roadmap = []
    total_days = 0

    for skill in missing_skills:
        info = ROADMAP.get(
            skill,
            {
                "level": "Intermediate",
                "days": 7,
            },
        )

        roadmap.append(
            {
                "skill": skill,
                "level": info["level"],
                "days": info["days"],
            }
        )

        total_days += info["days"]

    career_readiness = max(0, 100 - len(missing_skills) * 10)

    return {
        "roadmap": roadmap,
        "estimated_days": total_days,
        "career_readiness": career_readiness,
    }