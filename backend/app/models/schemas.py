"""
Pydantic models for request and response data structures
"""
from pydantic import BaseModel, Field
from typing import Optional


class JobDescriptionInput(BaseModel):
    """
    Model for job description input
    """
    job_title: str = Field(..., description="Job title for the position")
    job_description: str = Field(..., description="Detailed job description text")
    company_name: Optional[str] = Field(None, description="Name of the company")


class ResumeUploadResponse(BaseModel):
    """
    Model for resume upload response
    """
    message: str = Field(..., description="Response message")
    filename: str = Field(..., description="Name of the uploaded file")
    text_length: int = Field(..., description="Length of extracted text")
    extracted_text_preview: str = Field(..., description="Preview of extracted text")


class JobDescriptionResponse(BaseModel):
    """
    Model for job description response
    """
    message: str = Field(..., description="Response message")
    job_title: str = Field(..., description="Job title")
    description_length: int = Field(..., description="Length of job description")


class HealthResponse(BaseModel):
    """
    Model for health check response
    """
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Health check message")
