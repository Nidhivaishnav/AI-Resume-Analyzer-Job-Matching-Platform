"""
Main FastAPI application for AI Resume Analyzer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume_routes
from app.models.schemas import HealthResponse


# Initialize FastAPI application
app = FastAPI(
    title="AI Resume Analyzer & Job Matching Platform",
    description="API for analyzing resumes and matching them with job descriptions using AI/ML",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
# NOTE: allow_origins=["*"] is for development only
# In production, replace with specific allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_routes.router)


@app.get("/", response_model=HealthResponse, tags=["Health Check"])
async def root():
    """
    Root endpoint for health check
    
    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy",
        message="AI Resume Analyzer API is running successfully"
    )


@app.get("/health", response_model=HealthResponse, tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify service availability
    
    Returns:
        HealthResponse: Current service health status
    """
    return HealthResponse(
        status="healthy",
        message="Service is operational"
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # Host: 0.0.0.0 allows external access
    # Port: 8000 is the default port
    # Reload: True enables auto-reload during development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
