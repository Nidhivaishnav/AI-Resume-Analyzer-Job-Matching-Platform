"""
API routes for resume and job description operations
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.schemas import (
    JobDescriptionInput,
    ResumeUploadResponse,
    JobDescriptionResponse
)
from app.services.pdf_service import PDFExtractionService


# Create API router
router = APIRouter(prefix="/api/v1", tags=["Resume & Job Analysis"])

# Initialize PDF extraction service
pdf_service = PDFExtractionService()


@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(
    resume: UploadFile = File(..., description="Resume PDF file to upload")
):
    """
    Upload a resume PDF file and extract text content
    
    Args:
        resume: PDF file uploaded by the user
        
    Returns:
        ResumeUploadResponse: Contains extracted text information
        
    Raises:
        HTTPException: If file validation or text extraction fails
    """
    # Validate file type
    if not resume.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        # Read file content
        file_content = await resume.read()
        
        # Validate PDF file
        if not pdf_service.validate_pdf_file(file_content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid PDF file"
            )
        
        # Reset file pointer for extraction
        await resume.seek(0)
        
        # Extract text from PDF
        extracted_text = pdf_service.extract_text_from_pdf(resume.file)
        
        # Create preview (first 500 characters)
        text_preview = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        
        return ResumeUploadResponse(
            message="Resume uploaded and processed successfully",
            filename=resume.filename,
            text_length=len(extracted_text),
            extracted_text_preview=text_preview
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error internally (in production, use proper logging)
        print(f"Error processing resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing resume. Please ensure the file is a valid PDF."
        )


@router.post("/submit-job-description", response_model=JobDescriptionResponse)
async def submit_job_description(job_data: JobDescriptionInput):
    """
    Submit a job description for analysis
    
    Args:
        job_data: Job description information including title and description
        
    Returns:
        JobDescriptionResponse: Confirmation of job description submission
        
    Raises:
        HTTPException: If job description validation fails
    """
    # Validate job description length
    if len(job_data.job_description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is too short. Please provide a detailed description."
        )
    
    if len(job_data.job_title.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job title is too short"
        )
    
    try:
        # Process and store job description (placeholder for future implementation)
        # In production, this would save to database or temporary storage
        
        return JobDescriptionResponse(
            message="Job description submitted successfully",
            job_title=job_data.job_title,
            description_length=len(job_data.job_description)
        )
    
    except Exception as e:
        # Log the error internally (in production, use proper logging)
        print(f"Error processing job description: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing job description. Please try again."
        )
