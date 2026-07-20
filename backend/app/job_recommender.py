from .resume_matcher import match_resume


def recommend_jobs(resume_text, top_n=5):
    matches = match_resume(resume_text)

    matches = sorted(
        matches,
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches[:top_n]