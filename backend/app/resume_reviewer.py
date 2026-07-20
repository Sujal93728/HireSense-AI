import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def review_resume(resume_text):

    client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

    prompt = f"""
You are an ATS Resume Expert.

Analyze this resume.

Resume:

{resume_text}

Return ONLY valid JSON.

Format:

{{
"ats_score":0,
"summary":"",
"strengths":[],
"weaknesses":[],
"missing_skills":[],
"missing_keywords":[],
"recommended_projects":[],
"certifications":[],
"career_path":"",
"improvements":[]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return json.loads(
        response.choices[0].message.content
    )