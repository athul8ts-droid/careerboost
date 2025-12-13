import re

# -----------------------------
# 1. SKILL LIST (can expand anytime)
# -----------------------------
SKILL_LIST = [
    "python", "django", "flask", "fastapi", "java", "c", "c++", "c#", "javascript",
    "react", "node", "html", "css", "bootstrap", "sql", "mysql", "postgresql",
    "mongodb", "git", "github", "rest api", "aws", "azure", "machine learning",
    "data analysis", "power bi", "tableau", "excel", "communication", "teamwork",
    "leadership", "problem solving", "linux", "docker", "kubernetes"
]

# -----------------------------
# 2. Extract skills from resume text
# -----------------------------
def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        if skill in resume_text:
            found_skills.append(skill)

    return list(set(found_skills))

# -----------------------------
# 3. Extract keywords from job description
# -----------------------------
def extract_keywords(job_description):
    text = job_description.lower()

    # Split job description into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)

    # Filter meaningful keywords (skills only)
    job_keywords = [w for w in words if w in SKILL_LIST]

    return list(set(job_keywords))

# -----------------------------
# 4. Missing skill detection
# -----------------------------
def detect_missing_skills(resume_skills, job_keywords):
    resume_set = set(resume_skills)
    job_set = set(job_keywords)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    return matched, missing

# -----------------------------
# 5. Match percentage
# -----------------------------
def calculate_match_percentage(matched_skills, job_keywords):
    if len(job_keywords) == 0:
        return 0

    return round((len(matched_skills) / len(job_keywords)) * 100)

# -----------------------------
# 6. Full AI Scoring Function
# -----------------------------
def ai_score_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_keywords = extract_keywords(job_description)
    matched, missing = detect_missing_skills(resume_skills, job_keywords)
    match_percent = calculate_match_percentage(matched, job_keywords)

    return {
        "resume_skills": resume_skills,
        "job_keywords": job_keywords,
        "matched": matched,
        "missing": missing,
        "match_percent": match_percent
    }
