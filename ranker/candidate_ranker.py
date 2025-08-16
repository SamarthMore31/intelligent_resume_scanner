import numpy as np
from sentence_transformers import SentenceTransformer, util
import re

class CandidateRanker:
    def __init__(self, candidate_data, skill_weights, jd_text):
        self.candidate_data = candidate_data
        self.skill_weights = skill_weights
        self.jd_text = jd_text
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _calculate_keyword_score(self, resume_text):
        """
        Calculates the keyword match score using a more forgiving method
        and returns the skills that were found.
        """
        score = 0
        matched_skills = []
        # Convert resume to lowercase once to make matching faster
        resume_text_lower = resume_text.lower()
        for skill, weight in self.skill_weights.items():
            # A simpler, more robust check for the skill's presence.
            # The \b ensures we match whole words only (e.g., 'java' not 'javascript').
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_text_lower):
                score += weight
                matched_skills.append(skill)
        return score, matched_skills

    def _calculate_semantic_score(self, resume_text):
        """Calculates the semantic similarity score."""
        jd_embedding = self.model.encode(self.jd_text, convert_to_tensor=True)
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        semantic_score = util.pytorch_cos_sim(jd_embedding, resume_embedding)
        return semantic_score.item() * 100

    def get_ranked_candidates(self):
        """Ranks candidates and includes the list of matched skills."""
        if not self.candidate_data:
            return []

        for candidate in self.candidate_data:
            resume_text = candidate['resume_text']
            
            keyword_score, matched_skills = self._calculate_keyword_score(resume_text)
            semantic_score = self._calculate_semantic_score(resume_text)
            
            # Weighted final score (70% keyword, 30% semantic)
            final_score = (0.7 * keyword_score) + (0.3 * semantic_score)

            candidate['keyword_score'] = round(keyword_score, 2)
            candidate['semantic_score'] = round(semantic_score, 2)
            candidate['final_score'] = round(final_score, 2)
            candidate['matched_skills'] = matched_skills

        ranked_candidates = sorted(
            self.candidate_data, 
            key=lambda x: x['final_score'], 
            reverse=True
        )
        return ranked_candidates