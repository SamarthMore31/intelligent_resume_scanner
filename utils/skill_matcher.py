import re

def match_skills_from_text(resume_text, jd_skills):
    matched = []
    resume_text = resume_text.lower()

    for skill in jd_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_text):
            matched.append(skill)

    return matched
