"""
Utility functions for resume and job description analysis.

Includes:
- Skill extraction using keyword matching
- ATS score calculation based on resume vs job description
"""

import re


# ============================================================
# SKILL KEYWORDS
# ============================================================
SKILL_KEYWORDS = [
    "python", "django", "flask", "sql", "mysql", "postgresql",
    "machine learning", "data analysis", "pandas", "numpy",
    "html", "css", "javascript", "react",
    "api", "rest",
    "git", "github", "linux",
    "excel", "power bi", "tableau", "statistics"
]


# ============================================================
# SKILL EXTRACTION (USED FOR BOTH RESUME & JD)
# ============================================================
def extract_skills(text):
    """
    Extracts known skills from given text (resume or job description).

    Args:
        text (str): Raw text.

    Returns:
        list[str]: Unique list of matched skills.
    """
    if not text:
        return []

    text = text.lower()
    matched_skills = set()

    for skill in SKILL_KEYWORDS:
        # Handle multi-word skills safely
        if skill in text:
            matched_skills.add(skill)

    return sorted(matched_skills)


# ============================================================
# ATS SCORE CALCULATION
# ============================================================
def calculate_ats_score(resume_skills, jd_skills):
    """
    Calculates ATS score based on skill matching.

    Args:
        resume_skills (list[str]): Skills extracted from resume
        jd_skills (list[str]): Skills extracted from job description

    Returns:
        tuple:
            ats_score (float)
            matched_skills (list[str])
            missing_skills (list[str])
    """
    if not jd_skills:
        return 0.0, [], []

    resume_set = set(skill.lower() for skill in resume_skills)
    jd_set = set(skill.lower() for skill in jd_skills)

    matched_skills = sorted(resume_set & jd_set)
    missing_skills = sorted(jd_set - resume_set)

    ats_score = (len(matched_skills) / len(jd_set)) * 100

    return round(ats_score, 2), matched_skills, missing_skills
