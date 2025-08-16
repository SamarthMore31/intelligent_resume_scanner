import spacy
from collections import Counter
import re

# --- A COMPREHENSIVE & NOW CUSTOMIZED SKILL DATABASE ---
SKILL_DB = [
    # Programming & Software
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'go', 'rust', 'kotlin', 'swift', 'php', 'ruby', 'scala',
    'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'ruby on rails', '.net', 'express.js',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'sqlite', 'oracle', 'microsoft sql server',
    
    # Cloud & DevOps
    'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'git', 'ci/cd',
    
    # Data Science & AI
    'machine learning', 'deep learning', 'data analysis', 'data science', 'natural language processing', 'nlp', 'ai',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'spark', 'hadoop',
    
    # Telecommunications & IoT (NEW)
    '5g', 'iot', 'telecommunications', 'telecom', 'wireless', 'lte', 'rfp', 'pre-sales', 'solution design', 'automation',
    
    # Business & Other
    'agile', 'scrum', 'jira', 'linux', 'rest', 'graphql', 'api', 'html', 'css', 'sass', 'less', 'cybersecurity',
    'g-suite', 'documentation', 'pitch decks'
]

def extract_skills_from_jd(jd_text):
    """
    Extracts skills from the job description using a comprehensive skill list.
    """
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(jd_text.lower())
    
    found_skills = []
    
    # Use regex to find whole-word matches for skills from the SKILL_DB
    for skill in SKILL_DB:
        # The \b ensures we match 'java' but not 'javascript' if we only want 'java'
        if re.search(r'\b' + re.escape(skill) + r'\b', jd_text.lower()):
            found_skills.append(skill)
            
    # If no skills are found, return empty values to prevent errors
    if not found_skills:
        return [], {}

    # Count the frequency of each skill to use as a weight
    skill_weights = Counter(found_skills)
    
    # Return unique skills and their weights
    return list(skill_weights.keys()), dict(skill_weights)