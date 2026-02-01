"""
Job Matcher Module
Implements resume-job matching using TF-IDF and Sentence Transformers
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Tuple
import logging

# Configure logging
logger = logging.getLogger(__name__)


class JobMatcher:
    """Match resumes with job descriptions using multiple methods"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Initialize Sentence Transformer model (lightweight)
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence Transformer model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load sentence transformer: {e}. Semantic matching will be disabled.")
            self.sentence_model = None
    
    def calculate_tfidf_similarity(
        self, 
        resume_text: str, 
        job_description: str
    ) -> float:
        """Calculate similarity using TF-IDF and cosine similarity"""
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error in TF-IDF calculation: {e}")
            return 0.0
    
    def calculate_semantic_similarity(
        self, 
        resume_text: str, 
        job_description: str
    ) -> float:
        """Calculate similarity using Sentence Transformers"""
        if not self.sentence_model:
            return 0.0
        
        try:
            # Generate embeddings
            embeddings = self.sentence_model.encode([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                embeddings[0].reshape(1, -1),
                embeddings[1].reshape(1, -1)
            )[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error in semantic similarity calculation: {e}")
            return 0.0
    
    def match_resume_to_job(
        self, 
        resume_text: str, 
        job_description: str,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Dict:
        """
        Comprehensive matching between resume and job description
        Returns match score and details
        """
        # Calculate different similarity scores
        tfidf_score = self.calculate_tfidf_similarity(resume_text, job_description)
        semantic_score = self.calculate_semantic_similarity(resume_text, job_description)
        
        # Skill-based matching
        skill_match_score = self._calculate_skill_match(resume_skills, job_skills)
        
        # Combined score (weighted average)
        combined_score = (
            0.3 * tfidf_score +
            0.4 * semantic_score +
            0.3 * skill_match_score
        )
        
        # Find missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))
        matching_skills = list(set(job_skills) & set(resume_skills))
        
        return {
            "overall_score": round(combined_score * 100, 2),
            "tfidf_score": round(tfidf_score * 100, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "skill_match_score": round(skill_match_score * 100, 2),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "total_job_skills": len(job_skills),
            "matched_skills_count": len(matching_skills)
        }
    
    def _calculate_skill_match(
        self, 
        resume_skills: List[str], 
        job_skills: List[str]
    ) -> float:
        """Calculate skill match percentage"""
        if not job_skills:
            return 0.0
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matching = len(set(resume_skills_lower) & set(job_skills_lower))
        total = len(job_skills_lower)
        
        return matching / total if total > 0 else 0.0
    
    def rank_candidates(
        self, 
        candidates: List[Dict], 
        job_description: str
    ) -> List[Dict]:
        """
        Rank multiple candidates against a job description
        Each candidate should have 'resume_text' and 'resume_skills'
        """
        ranked = []
        
        for candidate in candidates:
            score = self.calculate_semantic_similarity(
                candidate.get('resume_text', ''),
                job_description
            )
            candidate['match_score'] = round(score * 100, 2)
            ranked.append(candidate)
        
        # Sort by match score (descending)
        ranked.sort(key=lambda x: x['match_score'], reverse=True)
        
        return ranked
