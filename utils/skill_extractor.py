# utils/skill_extractor.py

import spacy
from spacy.matcher import PhraseMatcher

# Let's build a simple skills database to detect from text.
# Ideally, use a big curated list. Here’s a sample:
SKILL_DB = [
    "python", "machine learning", "deep learning", "tensorflow", "pytorch",
    "sql", "c++", "java", "communication", "data analysis", "nlp",
    "computer vision", "docker", "kubernetes", "aws", "azure"
]

class SkillExtractor:
    def __init__(self, nlp, skill_list, PhraseMatcherAttr="LOWER"):
        self.nlp = nlp
        self.matcher = PhraseMatcher(nlp.vocab, attr=PhraseMatcherAttr)
        patterns = [nlp(skill) for skill in skill_list]
        self.matcher.add("SKILLS", patterns)

    def annotate(self, doc):
        matches = self.matcher(doc)
        results = []
        for match_id, start, end in matches:
            span = doc[start:end]
            results.append({"skill_name": span.text})
        return {"results": {"full_matches": results}}

import re

def extract_skills_from_jd(jd_text):
    # Simple list of predefined skills (could come from a skill dictionary or ML model)
    base_skills = [
        "python", "java", "machine learning", "deep learning", "communication", "data analysis",
        "pandas", "numpy", "tensorflow", "pytorch", "sql", "cloud", "aws", "azure", "nlp", 
        "cv", "computer vision", "project management", "excel", "data visualization"
    ]
    
    jd_text_lower = jd_text.lower()
    extracted = {}
    for skill in base_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', jd_text_lower):
            extracted[skill.lower()] = 1  # assign equal weight initially

    return extracted

def extract_skills_from_text(text: str, jd_skills: list) -> list:
    text = text.lower()
    jd_skills_lower = [skill.lower() for skill in jd_skills]
    matched = [skill for skill in jd_skills_lower if skill in text]
    return matched
