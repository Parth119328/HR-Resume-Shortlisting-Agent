def calculateMatchScore(jd_data, resume_data):
    jd_skills = set(
        skill.lower()
        for skill in jd_data.get("skills", [])
    )

    resume_skills = set(
        skill.lower()
        for skill in resume_data.get("skills", [])
    )

    matched_skills = list(jd_skills.intersection(resume_skills))

    missing_skills = list(jd_skills.difference(resume_skills))

    if len(jd_skills) > 0:
        skill_match_score = (len(matched_skills)/len(jd_skills)) * 100
    else:
        skill_match_score = 0

    experience_score = 0

    jd_experience = (
        jd_data.get(
            "experience", ""
        ).lower()
    )

    resume_experience = (
        resume_data.get(
            "experience", ""
        ).lower()
    )

    if jd_experience and resume_experience:
        if "5" in jd_experience and "5" in resume_experience:
            experience_score = 100
        elif "3" in jd_experience and "3" in resume_experience:
            experience_score = 100
        else:
            experience_score = 50

    education_score = 0
    jd_education = (
        jd_data.get(
            "education",
            ""
        ).lower()
    )

    resume_education = (
        resume_data.get(
            "education", ""
        ).lower()
    )

    if jd_education and resume_education:
        if ("computer science" in jd_education and "computer science" in resume_education):
            education_score = 100
        else:
            education_score = 60

    final_score = (
        (skill_match_score * 0.6) + (experience_score * 0.25) + (education_score * 0.15)
    )

    if final_score >= 80:
        recommendation = "Strong Match"
    elif final_score >= 60:
        recommendation = "Good Match"
    elif final_score >= 40:
        recommendation = "Average Match"
    else:
        recommendation = "Low Match"

    return {
        "match_score": round(final_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }
