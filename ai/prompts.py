#JD PROMPT
JD_EXTRACTION_PROMPT = """
You are an expert HR assistant.

Analyze the following Job Description carefully.

Extract:

1. Required skills
2. Required experience
3. Required education
4. Important keywords
5. Job role/title

Return ONLY valid JSON.

Format:

{
    "job_role": "",
    "skills": [],
    "experience": "",
    "education": "",
    "keywords": []
}

Job Description:
"""


#RESUME PROMPT
RESUME_EXTRACTION_PROMPT = """
You are an expert HR resume analyzer.

Analyze the following resume carefully.

Extract:

1. Candidate name
2. Skills
3. Years of experience
4. Education
5. Projects
6. Certifications
7. Resume summary

Return ONLY valid JSON.

Format:

{
    "name": "",
    "skills": [],
    "experience": "",
    "education": "",
    "projects": [],
    "certifications": [],
    "summary": ""
}

Resume:
"""