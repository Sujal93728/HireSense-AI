import re

# Common technical skills
SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "react",
    "reactjs",
    "node",
    "nodejs",
    "express",
    "fastapi",
    "flask",
    "django",
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "opencv",
    "rest",
    "rest api",
    "api",
    "graphql",
    "firebase",
    "figma"
}


def extract_skills(text):
    """
    Extract skills from resume or job description.
    """

    if not text:
        return []

    text = text.lower()

    found = set()

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.add(skill.title())

    return sorted(list(found))


def compare_skills(resume_text, job_description):
    """
    Compare resume skills with job skills.
    """

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched = sorted(list(resume_skills & job_skills))
    missing = sorted(list(job_skills - resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100, 2)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }