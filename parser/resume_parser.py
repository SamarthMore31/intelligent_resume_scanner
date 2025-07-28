import spacy
import re
from utils.pdf_reader import extract_text_from_pdf
from utils.skill_matcher import match_skills_from_text

nlp = spacy.load("en_core_web_sm")

# Helper function: checks if it looks like a real name
def looks_like_name(name):
    return (
        len(name.split()) >= 2 and
        all(part.isalpha() for part in name.split()) and
        name.lower() not in ["curriculum vitae", "resume", "project", "trained", "model", "notebook", "python", "radar", "ai", "ml"]
    )

def extract_name(text):
    doc = nlp(text)
    people = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

    for name in people:
        if looks_like_name(name) and len(name) < 60:
            return name

    # fallback: scan first few lines manually
    lines = text.strip().split("\n")[:10]
    for line in lines:
        line = line.strip()
        if looks_like_name(line):
            return line
    return "Unknown"

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0).strip() if match else ""

def parse_resume(resume_path, jd_skills):
    text = extract_text_from_pdf(resume_path)

    name = extract_name(text)
    email = extract_email(text)
    matched_skills = match_skills_from_text(text, jd_skills)

    # Debug logs
    print("📄 Resume Path:", resume_path)
    print("👤 Extracted Name:", name)
    print("✉️ Email:", email)
    print("🔍 JD SKILLS:", jd_skills)
    print("🎯 Matched Skills:", matched_skills)
    print("=" * 40)

    return {
        "name": name,
        "email": email,
        "skills": matched_skills
    }
