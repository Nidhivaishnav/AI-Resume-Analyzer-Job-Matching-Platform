"""
Skill Extractor Module
Uses spaCy NLP for extracting skills and analyzing text
"""
import spacy
from typing import List, Set
import re


class SkillExtractor:
    """Extract skills from text using NLP and pattern matching"""
    
    def __init__(self):
        # Common skills database (can be extended)
        self.skill_patterns = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 
            'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'fastapi', 'spring', 'asp.net',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
            'cassandra', 'dynamodb', 'elasticsearch',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'terraform', 'ansible', 'ci/cd', 'git', 'github', 'gitlab',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'scikit-learn', 'pandas', 'numpy', 'nlp', 'computer vision',
            'data analysis', 'data science', 'ai', 'artificial intelligence',
            
            # Other Technical Skills
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum',
            'testing', 'unit testing', 'linux', 'bash', 'shell scripting'
        }
        
        try:
            # Load spaCy English model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not installed, will use pattern matching only
            self.nlp = None
            print("Warning: spaCy model not loaded. Using pattern matching only.")
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = set()
        
        # Pattern-based matching
        for skill in self.skill_patterns:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # NLP-based extraction (if available)
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract noun phrases that might be skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower().strip()
                # Check if it matches known skills
                if chunk_text in self.skill_patterns:
                    found_skills.add(chunk_text)
        
        return sorted(list(found_skills))
    
    def extract_entities(self, text: str) -> dict:
        """Extract named entities from text"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        return entities
    
    def get_key_phrases(self, text: str, top_n: int = 10) -> List[str]:
        """Extract key phrases from text"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        
        # Extract noun chunks as key phrases
        phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Return unique phrases
        unique_phrases = list(dict.fromkeys(phrases))
        return unique_phrases[:top_n]
