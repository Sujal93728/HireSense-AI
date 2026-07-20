from .skill_extractor import extract_skills


def compare_skills(
    resume_text,
    job_description
):
    resume = set(extract_skills(resume_text))
    job = set(extract_skills(job_description))

    return {
        "matching_skills": list(resume & job),
        "missing_skills": list(job - resume)
    }