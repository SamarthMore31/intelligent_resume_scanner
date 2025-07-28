from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
from utils.skill_extractor import extract_skills_from_jd  # <-- NEW

class CandidateRanker:
    def __init__(self, jd_text: str):
        # 🔍 Extract weighted skills directly from JD
        self.jd_skill_weights = extract_skills_from_jd(jd_text)
        self.total_weight = sum(self.jd_skill_weights.values())

        # 🤖 Load sentence transformer for semantic similarity
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def weighted_skill_score(self, candidate_skills: List[str]) -> float:
        # Normalize JD skills for case-insensitive matching
        normalized_jd_skills = {k.lower(): v for k, v in self.jd_skill_weights.items()}
        candidate_skills_set = set(skill.lower() for skill in candidate_skills)
        matched_weights = sum(normalized_jd_skills.get(skill, 0) for skill in candidate_skills_set)
        return matched_weights / self.total_weight if self.total_weight > 0 else 0

    def semantic_similarity_score(self, jd_skills_text: str, candidate_skills_list: List[str]) -> float:
        if not candidate_skills_list:
            return 0.0  # Avoid embedding empty strings

        jd_embedding = self.embedder.encode(jd_skills_text, convert_to_tensor=True)
        candidate_text = " ".join(candidate_skills_list)
        candidate_embedding = self.embedder.encode(candidate_text, convert_to_tensor=True)

        cosine_sim = util.pytorch_cos_sim(jd_embedding, candidate_embedding)
        return cosine_sim.item()

    def score_candidate(self, candidate_skills: List[str]) -> float:
        if not candidate_skills:
            return 0.0

        jd_skills_text = " ".join(self.jd_skill_weights.keys())
        weight_score = self.weighted_skill_score(candidate_skills)
        sim_score = self.semantic_similarity_score(jd_skills_text, candidate_skills)

        final_score = 0.7 * weight_score + 0.3 * sim_score

        return final_score

    def rank_candidates(self, candidates: List[Dict]) -> List[Dict]:
        for candidate in candidates:
            candidate['score'] = self.score_candidate(candidate.get('skills', []))

            # 🧪 Debug logs (optional but great for testing)
            print(f"\n📋 Ranking Candidate: {candidate.get('name', 'Unknown')}")
            print(f"💬 Skills: {candidate.get('skills', [])}")
            print(f"⭐ Final Score: {candidate['score']:.4f}")
            print("-" * 40)

        ranked = sorted(candidates, key=lambda x: x['score'], reverse=True)
        return ranked