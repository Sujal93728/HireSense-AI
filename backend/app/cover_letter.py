def generate_cover_letter(job, resume_analysis):
    strengths = ", ".join(resume_analysis.get("strengths", []))

    letter = f"""
Dear Hiring Manager,

I am excited to apply for the {job.title} position.

My background and technical skills make me a strong candidate for this role.

Some of my key strengths include:

{strengths}

I am passionate about learning new technologies and contributing to impactful projects. I believe my skills align well with your requirements.

Thank you for considering my application.

Sincerely,
Candidate
"""

    return {
        "cover_letter": letter.strip()
    }