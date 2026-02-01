"""
FastAPI Main Application
Provides REST API endpoints for resume analysis and job matching
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from typing import Optional

from app.core.resume_parser import ResumeParser
from app.core.skill_extractor import SkillExtractor
from app.core.job_matcher import JobMatcher
from app.core.llm_feedback import FeedbackGenerator
from app.models.schemas import (
    ResumeAnalysisResponse, 
    MatchResult, 
    FeedbackResponse,
    JobDescription
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer & Job Matching Platform",
    description="Analyze resumes, extract skills, and match with job descriptions using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()
job_matcher = JobMatcher()
feedback_generator = FeedbackGenerator()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume Analyzer & Job Matching Platform API",
        "version": "1.0.0",
        "endpoints": {
            "analyze_resume": "/api/analyze-resume",
            "match_job": "/api/match-job",
            "get_feedback": "/api/get-feedback"
        }
    }


@app.post("/api/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a resume PDF file
    - Extracts text, contact information
    - Identifies skills using NLP
    - Returns structured analysis
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse resume
        parsed_data = resume_parser.parse(str(file_path))
        
        # Extract skills
        skills = skill_extractor.extract_skills(parsed_data["text"])
        
        # Extract key phrases
        key_phrases = skill_extractor.get_key_phrases(parsed_data["text"])
        
        # Clean up
        os.remove(file_path)
        
        return ResumeAnalysisResponse(
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            extracted_skills=skills,
            key_phrases=key_phrases,
            text_preview=parsed_data["text"][:500]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@app.post("/api/match-job", response_model=MatchResult)
async def match_job(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Match a resume against a job description
    - Calculates multiple similarity scores
    - Identifies matching and missing skills
    - Returns comprehensive match analysis
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save and parse resume
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        parsed_data = resume_parser.parse(str(file_path))
        resume_skills = skill_extractor.extract_skills(parsed_data["text"])
        
        # Extract job skills
        job_skills = skill_extractor.extract_skills(job_description)
        
        # Perform matching
        match_result = job_matcher.match_resume_to_job(
            resume_text=parsed_data["text"],
            job_description=job_description,
            resume_skills=resume_skills,
            job_skills=job_skills
        )
        
        # Clean up
        os.remove(file_path)
        
        return MatchResult(**match_result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching job: {str(e)}")


@app.post("/api/get-feedback", response_model=FeedbackResponse)
async def get_feedback(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Get AI-powered feedback on resume
    - Analyzes resume against job description
    - Provides improvement suggestions
    - Offers skill development guidance
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save and parse resume
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        parsed_data = resume_parser.parse(str(file_path))
        resume_skills = skill_extractor.extract_skills(parsed_data["text"])
        
        # Extract job skills
        job_skills = skill_extractor.extract_skills(job_description)
        
        # Perform matching
        match_result = job_matcher.match_resume_to_job(
            resume_text=parsed_data["text"],
            job_description=job_description,
            resume_skills=resume_skills,
            job_skills=job_skills
        )
        
        # Generate AI feedback
        feedback = feedback_generator.generate_resume_feedback(
            resume_text=parsed_data["text"],
            job_description=job_description,
            match_score=match_result["overall_score"]
        )
        
        # Generate skill suggestions
        skill_suggestions = feedback_generator.suggest_missing_skills(
            missing_skills=match_result["missing_skills"],
            resume_text=parsed_data["text"],
            job_description=job_description
        )
        
        # Clean up
        os.remove(file_path)
        
        return FeedbackResponse(
            resume_feedback=feedback,
            skill_suggestions=skill_suggestions,
            match_result=MatchResult(**match_result)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating feedback: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
