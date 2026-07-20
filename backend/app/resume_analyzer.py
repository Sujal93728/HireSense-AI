import re


ACTION_WORDS = [
    "developed",
    "built",
    "designed",
    "implemented",
    "optimized",
    "created",
    "managed",
    "improved",
    "deployed",
    "engineered"
]


def analyze_resume(text):

    text = text.lower()

    score = 50

    suggestions = []

    strengths = []

    weaknesses = []

    # Education
    if "b.tech" in text or "bachelor" in text:
        score += 10
        strengths.append("Education section found")
    else:
        weaknesses.append("Education section missing")

    # Projects
    if "project" in text:
        score += 10
        strengths.append("Projects included")
    else:
        weaknesses.append("Add projects")

    # Skills
    if "skills" in text:
        score += 10
        strengths.append("Skills section present")
    else:
        weaknesses.append("Add a skills section")

    # GitHub
    if "github" in text:
        score += 5
    else:
        suggestions.append("Add GitHub profile")

    # LinkedIn
    if "linkedin" in text:
        score += 5
    else:
        suggestions.append("Add LinkedIn profile")

    # Action words
    action_count = 0

    for word in ACTION_WORDS:
        if word in text:
            action_count += 1

    if action_count >= 5:
        score += 10
        strengths.append("Strong action verbs")
    else:
        suggestions.append("Use stronger action verbs")

    score = min(score, 100)

    return {
        "resume_score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }