# Quick Start Guide - AI Resume Analyzer Backend

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation & Running

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python main.py
   ```
   
   The server will start on `http://localhost:8000`

5. **Access the API documentation:**
   - Open your browser and navigate to `http://localhost:8000/docs`
   - You'll see the interactive Swagger UI where you can test all endpoints

## Testing the Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Upload Resume
```bash
curl -X POST http://localhost:8000/api/v1/upload-resume \
  -F "resume=@path/to/your/resume.pdf"
```

### 3. Submit Job Description
```bash
curl -X POST http://localhost:8000/api/v1/submit-job-description \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "job_description": "Detailed job description here...",
    "company_name": "Company Name"
  }'
```

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
└── app/
    ├── models/            # Pydantic schemas
    ├── routes/            # API endpoints
    ├── services/          # Business logic (PDF extraction, etc.)
    └── utils/             # Helper functions
```

## Next Steps
- Add database integration for storing resumes and job descriptions
- Implement AI/ML models for resume analysis
- Add user authentication
- Implement skill extraction and matching algorithms

## Troubleshooting

**Port already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Module not found errors:**
Make sure you've activated your virtual environment and installed all dependencies.

**PDF upload fails:**
Ensure the file is a valid PDF and not corrupted.
