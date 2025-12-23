"""
Utility functions for resume processing.

Currently includes basic skill extraction logic
based on predefined keyword matching.
"""

import re


# ============================================================
# SKILL KEYWORDS
# ============================================================
# List of commonly used technical skills.
# This can be expanded or replaced with a database / ML model later.
SKILL_KEYWORDS = [
    "python", "django", "flask", "sql", "mysql", "postgresql",
    "machine learning", "data analysis", "pandas", "numpy",
    "html", "css", "javascript", "react", "api", "rest",
    "git", "github", "linux",
]


# ============================================================
# SKILL EXTRACTION
# ============================================================
def extract_skills(text):
    """
    Extracts known skills from resume text.

    Args:
        text (str): Raw resume text.

    Returns:
        list[str]: Unique list of matched skills.
    """
    if not text:
        return []

    text = text.lower()
    matched_skills = []

    for skill in SKILL_KEYWORDS:
        # Use word boundaries to avoid partial matches
        if re.search(rf"\b{re.escape(skill)}\b", text):
            matched_skills.append(skill)

    return list(set(matched_skills))
