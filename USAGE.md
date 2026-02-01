# Usage Examples

This document provides examples of how to use the AI Resume Analyzer & Job Matching Platform.

## Table of Contents
1. [Starting the Application](#starting-the-application)
2. [Using the API](#using-the-api)
3. [Using the Dashboard](#using-the-dashboard)
4. [Docker Deployment](#docker-deployment)

## Starting the Application

### Method 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start API server
uvicorn app.main:app --reload

# In a new terminal, start dashboard
streamlit run app/dashboard.py
```

### Method 2: Using Setup Script

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
uvicorn app.main:app --reload
```

## Using the API

### Example 1: Analyze Resume

```python
import requests

url = "http://localhost:8000/api/analyze-resume"

with open("my_resume.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    
result = response.json()
print(f"Name: {result['name']}")
print(f"Email: {result['email']}")
print(f"Skills: {', '.join(result['extracted_skills'])}")
```

### Example 2: Match Resume with Job

```python
import requests

url = "http://localhost:8000/api/match-job"

job_desc = """
We are looking for a Senior Python Developer with experience in:
- Python, Django, FastAPI
- Docker, Kubernetes
- AWS or Azure
- Machine Learning
- REST API development
"""

with open("my_resume.pdf", "rb") as f:
    files = {"file": f}
    data = {"job_description": job_desc}
    response = requests.post(url, files=files, data=data)
    
result = response.json()
print(f"Match Score: {result['overall_score']}%")
print(f"Matching Skills: {result['matching_skills']}")
print(f"Missing Skills: {result['missing_skills']}")
```

### Example 3: Get AI Feedback

```python
import requests

url = "http://localhost:8000/api/get-feedback"

job_desc = """
Full Stack Developer position requiring:
- React, Node.js, TypeScript
- MongoDB, PostgreSQL
- Docker, CI/CD
- 3+ years experience
"""

with open("my_resume.pdf", "rb") as f:
    files = {"file": f}
    data = {"job_description": job_desc}
    response = requests.post(url, files=files, data=data)
    
result = response.json()
print("Resume Feedback:")
print(result['resume_feedback'])
print("\nSkill Suggestions:")
print(result['skill_suggestions'])
```

## Using the Dashboard

1. **Navigate to Dashboard**
   ```
   http://localhost:8501
   ```

2. **Resume Analysis**
   - Select "Resume Analysis" from sidebar
   - Upload your PDF resume
   - Click "Analyze Resume"
   - View extracted information and skills

3. **Job Matching**
   - Select "Job Matching" from sidebar
   - Upload your resume
   - Paste job description
   - Click "Calculate Match"
   - Review match scores and skill gaps

4. **AI Feedback**
   - Select "AI Feedback" from sidebar
   - Upload your resume
   - Paste job description
   - Click "Get AI Feedback"
   - Read personalized recommendations

## Docker Deployment

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Services

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Environment Variables

Create a `.env` file for production:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
DASHBOARD_PORT=8501
```

## API Endpoints Reference

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Analyze Resume
```bash
curl -X POST "http://localhost:8000/api/analyze-resume" \
  -F "file=@resume.pdf"
```

### 3. Match Job
```bash
curl -X POST "http://localhost:8000/api/match-job" \
  -F "file=@resume.pdf" \
  -F "job_description=Looking for Python developer with ML experience..."
```

### 4. Get Feedback
```bash
curl -X POST "http://localhost:8000/api/get-feedback" \
  -F "file=@resume.pdf" \
  -F "job_description=Senior developer position..."
```

## Tips for Best Results

1. **Resume Format**
   - Use well-formatted PDF resumes
   - Include clear sections (skills, experience, education)
   - List technical skills explicitly

2. **Job Descriptions**
   - Paste complete job descriptions
   - Include required skills section
   - Add preferred qualifications

3. **AI Feedback**
   - Set OPENAI_API_KEY for enhanced feedback
   - Without API key, basic feedback is still provided
   - Be patient, LLM responses may take 10-30 seconds

4. **Skill Matching**
   - The system recognizes 100+ common technical skills
   - Skills are case-insensitive
   - Multi-word skills (e.g., "machine learning") are supported

## Troubleshooting

### Issue: "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### Issue: "Sentence transformer model not loading"
- Requires internet connection on first run
- Model is cached locally after first download
- Basic TF-IDF matching works without it

### Issue: "OpenAI API error"
- Check if OPENAI_API_KEY is set correctly
- Verify API key is valid and has credits
- System provides basic feedback without LLM

### Issue: "Port already in use"
```bash
# Change API port
uvicorn app.main:app --port 8001

# Change Streamlit port
streamlit run app/dashboard.py --server.port 8502
```

## Advanced Usage

### Batch Processing

```python
import os
import requests

def analyze_resumes_batch(resume_folder):
    """Analyze multiple resumes"""
    results = []
    
    for filename in os.listdir(resume_folder):
        if filename.endswith('.pdf'):
            filepath = os.path.join(resume_folder, filename)
            
            with open(filepath, 'rb') as f:
                response = requests.post(
                    "http://localhost:8000/api/analyze-resume",
                    files={"file": f}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    result['filename'] = filename
                    results.append(result)
    
    return results

# Use it
resumes = analyze_resumes_batch("./resumes")
for resume in resumes:
    print(f"{resume['filename']}: {len(resume['extracted_skills'])} skills found")
```

### Custom Skill Patterns

You can extend the skill patterns in `app/core/skill_extractor.py`:

```python
self.skill_patterns = {
    # Add your custom skills
    'your_custom_skill',
    'another_skill',
    # ...
}
```
