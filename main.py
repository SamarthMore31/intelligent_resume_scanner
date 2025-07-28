# main.py

import os
from parser.resume_parser import parse_resume
from ranker.candidate_ranker import CandidateRanker
from utils.file_loader import load_jd_skills_with_weights
from csv import DictWriter

def save_ranking_to_csv(ranked_candidates, output_path='results/ranking_output.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'name', 'email', 'score', 'skills']
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rank, candidate in enumerate(ranked_candidates, 1):
            writer.writerow({
                'rank': rank,
                'name': candidate.get('name', ''),
                'email': candidate.get('email', ''),
                'score': f"{candidate.get('score', 0):.2f}",
                'skills': ", ".join(candidate.get('skills', []))
            })

def main():
    # ✅ Load JD skills with weights
    jd_path = 'data/jd.txt'
    jd_skills_with_weights = load_jd_skills_with_weights(jd_path)
    print("Job Description Skills Loaded (with weights):", jd_skills_with_weights)

    # 🧾 Parse all resumes in folder
    resumes_folder = 'data/resumes/'
    candidates = []
    for filename in os.listdir(resumes_folder):
        if filename.endswith('.pdf'):
            resume_path = os.path.join(resumes_folder, filename)
            candidate = parse_resume(resume_path, list(jd_skills_with_weights.keys()))
            candidates.append(candidate)

    # 🎯 Rank candidates using weighted skills
    ranker = CandidateRanker(jd_skills_with_weights)
    ranked_candidates = ranker.rank_candidates(candidates)

    # 📊 Print ranked results
    for i, cand in enumerate(ranked_candidates, 1):
        print(f"{i}. {cand['name']} - Score: {cand['score']:.2f}")

    # 💾 Save results
    save_ranking_to_csv(ranked_candidates)
    print("Ranking saved to results/ranking_output.csv")

if __name__ == "__main__":
    main()
