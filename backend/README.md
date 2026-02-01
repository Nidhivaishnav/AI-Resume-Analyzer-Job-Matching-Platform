# AI Resume Analyzer - Backend API

## Overview
This is the backend API for the AI Resume Analyzer & Job Matching Platform, built with FastAPI. It provides endpoints for uploading resumes, submitting job descriptions, and extracting text from PDF files.

## Project Structure
```
backend/
├── main.py                 # Main FastAPI application entry point
├── requirements.txt        # Python dependencies
└── app/
    ├── __init__.py        # App package initialization
    ├── models/            # Data models and schemas
    │   ├── __init__.py
    │   └── schemas.py     # Pydantic models for request/response
    ├── routes/            # API endpoints
    │   ├── __init__.py
    │   └── resume_routes.py  # Resume and job description routes
    ├── services/          # Business logic services
    │   ├── __init__.py
    │   └── pdf_service.py    # PDF text extraction service
    └── utils/             # Utility functions
        └── __init__.py
```

## Features
- ✅ Upload resume PDF files
- ✅ Extract text from PDF resumes
- ✅ Submit job descriptions
- ✅ REST API with automatic documentation
- ✅ CORS support for frontend integration
- ✅ Input validation with Pydantic
- ✅ Clean, modular architecture

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Base URL: http://localhost:8000
- Interactive API Documentation (Swagger UI): http://localhost:8000/docs
- Alternative Documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Health Check
- **GET** `/` - Root endpoint
- **GET** `/health` - Health check endpoint

### Resume & Job Analysis
- **POST** `/api/v1/upload-resume` - Upload a resume PDF file
  - Request: Multipart form data with PDF file
  - Response: Extracted text preview and metadata

- **POST** `/api/v1/submit-job-description` - Submit job description
  - Request: JSON with job title and description
  - Response: Confirmation with job details

## Usage Examples

### Upload Resume
```bash
curl -X POST "http://localhost:8000/api/v1/upload-resume" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@path/to/resume.pdf"
```

### Submit Job Description
```bash
curl -X POST "http://localhost:8000/api/v1/submit-job-description" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "job_description": "We are looking for an experienced software engineer...",
    "company_name": "Tech Corp"
  }'
```

## Development

### Code Structure
- **models/schemas.py**: Defines Pydantic models for request/response validation
- **services/pdf_service.py**: Handles PDF text extraction logic
- **routes/resume_routes.py**: Defines API endpoints and request handling
- **main.py**: Application initialization and configuration

### Adding New Features
1. Define data models in `app/models/schemas.py`
2. Implement business logic in `app/services/`
3. Create API endpoints in `app/routes/`
4. Register routes in `main.py`

## Future Enhancements
- [ ] Database integration for storing resumes and job descriptions
- [ ] AI/ML models for resume analysis
- [ ] Skill extraction and matching algorithms
- [ ] User authentication and authorization
- [ ] Rate limiting and security features
- [ ] Comprehensive test suite

## Dependencies
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **PyPDF2**: PDF text extraction library
- **Pydantic**: Data validation using Python type annotations
- **python-multipart**: Support for file uploads

## License
MIT License
