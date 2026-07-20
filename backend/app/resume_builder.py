def build_resume(data):
    return f"""
==============================
        PROFESSIONAL RESUME
==============================

Name:
{data.get("name")}

Email:
{data.get("email")}

Phone:
{data.get("phone")}

Location:
{data.get("location")}

--------------------------------

SUMMARY

{data.get("summary")}

--------------------------------

SKILLS

{", ".join(data.get("skills", []))}

--------------------------------

EXPERIENCE

{data.get("experience")}

--------------------------------

PROJECTS

{data.get("projects")}

--------------------------------

EDUCATION

{data.get("education")}

==============================
"""