"""
LLM Feedback Generator Module
Uses LangChain with OpenAI to generate resume feedback and suggestions
"""
from typing import Dict, List, Optional
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain not available. LLM features will be disabled.")

# Configuration constants
MAX_RESUME_TEXT_LENGTH = 3000  # Limit for resume text to stay within token limits
MAX_JOB_DESC_LENGTH = 2000     # Limit for job description to stay within token limits


class FeedbackGenerator:
    """Generate AI-powered resume feedback using LangChain and LLM"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if self.api_key and LANGCHAIN_AVAILABLE:
            try:
                self.llm = ChatOpenAI(
                    temperature=0.7,
                    model_name="gpt-3.5-turbo",
                    openai_api_key=self.api_key
                )
                self.llm_available = True
                logger.info("LLM initialized successfully with OpenAI")
            except Exception as e:
                logger.warning(f"Could not initialize LLM: {e}")
                self.llm_available = False
        else:
            if not LANGCHAIN_AVAILABLE:
                logger.warning("LangChain not available. LLM features will be disabled.")
            else:
                logger.info("No OpenAI API key provided. LLM features will be disabled.")
            self.llm_available = False
    
    def generate_resume_feedback(
        self, 
        resume_text: str, 
        job_description: str,
        match_score: float
    ) -> str:
        """Generate comprehensive feedback on resume"""
        if not self.llm_available:
            return self._generate_basic_feedback(match_score)
        
        try:
            prompt_text = f"""
            You are an expert career advisor and resume consultant. 
            
            Analyze the following resume against the job description and provide constructive feedback.
            
            Resume:
            {resume_text[:MAX_RESUME_TEXT_LENGTH]}
            
            Job Description:
            {job_description[:MAX_JOB_DESC_LENGTH]}
            
            Match Score: {match_score}%
            
            Please provide:
            1. Overall assessment of the resume quality
            2. How well the resume aligns with the job requirements
            3. Strengths of the resume
            4. Areas for improvement
            5. Specific suggestions to improve match score
            
            Keep the feedback professional, constructive, and actionable.
            """
            
            response = self.llm.invoke(prompt_text)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logger.error(f"Error generating LLM feedback: {e}")
            return self._generate_basic_feedback(match_score)
    
    def suggest_missing_skills(
        self, 
        missing_skills: List[str],
        resume_text: str,
        job_description: str
    ) -> str:
        """Generate suggestions for acquiring missing skills"""
        if not self.llm_available:
            return self._generate_basic_skill_suggestions(missing_skills)
        
        try:
            prompt_text = f"""
            You are a career development advisor helping someone improve their skills.
            
            The candidate is missing these skills for their target job:
            {', '.join(missing_skills)}
            
            Job Description:
            {job_description[:MAX_JOB_DESC_LENGTH]}
            
            Current Resume:
            {resume_text[:MAX_RESUME_TEXT_LENGTH]}
            
            Provide:
            1. Prioritization of which skills to learn first
            2. Learning resources for each skill (courses, certifications, books)
            3. Practical projects to demonstrate these skills
            4. Estimated time to acquire each skill
            5. How to highlight these skills once learned
            
            Be specific and actionable.
            """
            
            response = self.llm.invoke(prompt_text)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logger.error(f"Error generating skill suggestions: {e}")
            return self._generate_basic_skill_suggestions(missing_skills)
    
    def _generate_basic_feedback(self, match_score: float) -> str:
        """Fallback basic feedback when LLM is not available"""
        if match_score >= 70:
            return f"""
            Overall Assessment: Good Match ({match_score}%)
            
            Your resume shows a strong alignment with the job requirements. 
            
            Strengths:
            - Good skill match with job requirements
            - Relevant experience indicated
            
            Suggestions:
            - Review the missing skills section
            - Tailor your resume to highlight relevant achievements
            - Ensure keywords from job description are present
            """
        elif match_score >= 50:
            return f"""
            Overall Assessment: Moderate Match ({match_score}%)
            
            Your resume has some alignment with the job requirements but needs improvement.
            
            Areas for Improvement:
            - Add more relevant skills from the job description
            - Highlight projects and experiences that match job requirements
            - Consider adding certifications in missing skill areas
            
            Suggestions:
            - Focus on acquiring the missing critical skills
            - Restructure resume to emphasize relevant experience
            """
        else:
            return f"""
            Overall Assessment: Low Match ({match_score}%)
            
            Your resume needs significant updates to match this job position.
            
            Key Actions:
            - Acquire the missing skills listed in the analysis
            - Gain relevant experience through projects or courses
            - Consider if this role aligns with your career goals
            
            Suggestions:
            - Start with foundational skills from the missing skills list
            - Look for entry-level positions that match your current skill set
            - Build a portfolio demonstrating relevant skills
            """
    
    def _generate_basic_skill_suggestions(self, missing_skills: List[str]) -> str:
        """Fallback basic skill suggestions"""
        return f"""
        Missing Skills Priority Learning Plan:
        
        Skills to acquire: {', '.join(missing_skills)}
        
        General Recommendations:
        1. Start with the most in-demand skills in your industry
        2. Use online learning platforms (Coursera, Udemy, edX)
        3. Build projects to demonstrate each skill
        4. Consider certifications for key technologies
        5. Join communities and forums to stay updated
        
        Suggested approach:
        - Dedicate 1-2 hours daily to learning
        - Focus on one skill at a time
        - Build practical projects
        - Update your resume as you learn
        """
