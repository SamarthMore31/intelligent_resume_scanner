import os
import pandas as pd
from utils.file_loader import load_jd
from utils.pdf_reader import read_pdf
from parser.resume_parser import ResumeParser # <-- CHANGED
from ranker.candidate_ranker import CandidateRanker
from utils.skill_extractor import extract_skills_from_jd

def main():
    # Paths
    jd_path = 'data/job_description.txt'
    resumes_dir = 'data/resumes/'
    output_path = 'output/ranked_candidates.csv'

    # Load JD and extract skills/weights
    jd_text = load_jd(jd_path)
    if not jd_text:
        print(f"Error: Job description not found at {jd_path}")
        return

    jd_skills, skill_weights = extract_skills_from_jd(jd_text)
    if not jd_skills:
        print("Could not extract skills from the job description.")
        return

    # Process resumes
    candidate_data = []
    resume_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    
    print(f"Found {len(resume_files)} resumes to process...")

    for filename in resume_files:
        resume_path = os.path.join(resumes_dir, filename)
        resume_text = read_pdf(resume_path)
        
        if resume_text:
            parser = ResumeParser(resume_text) # <-- CHANGED
            details = parser.get_details()     # <-- CHANGED
            
            candidate_data.append({
                'name': details['name'] or "Not Found",
                'email': details['email'] or "Not Found",
                'resume_text': details['text'],
                'filename': filename
            })
    
    if not candidate_data:
        print("No candidates were processed. Check the resumes directory.")
        return

    # Rank candidates
    print("Ranking candidates...")
    ranker = CandidateRanker(candidate_data, skill_weights, jd_text)
    ranked_candidates = ranker.get_ranked_candidates()

    # Save to CSV
    df = pd.DataFrame(ranked_candidates)
    df.to_csv(output_path, index=False)

    print(f"Ranking complete! Results saved to {output_path}")

if __name__ == '__main__':
    main()