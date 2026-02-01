# AI Resume Analyzer & Job Matching Platform

A comprehensive Python-based AI application that analyzes resumes and job descriptions using NLP, ML, and LLMs. It extracts skills, computes semantic match scores, identifies skill gaps, and provides AI-driven resume feedback.

## 🌟 Features

- **Resume Parsing**: Extract text and metadata from PDF resumes
- **Skill Extraction**: Identify technical skills using spaCy NLP
- **Job Matching**: Calculate compatibility scores using TF-IDF and Sentence Transformers
- **Semantic Analysis**: Advanced matching with cosine similarity
- **AI Feedback**: LangChain-powered resume feedback and improvement suggestions
- **Interactive Dashboard**: User-friendly Streamlit interface
- **REST API**: FastAPI backend with comprehensive endpoints
- **Docker Support**: Easy deployment with Docker and docker-compose

## 🏗️ Architecture

```
├── app/
│   ├── core/              # Core business logic
│   │   ├── resume_parser.py      # PDF parsing
│   │   ├── skill_extractor.py    # NLP skill extraction
│   │   ├── job_matcher.py        # TF-IDF & Semantic matching
│   │   └── llm_feedback.py       # LangChain LLM integration
│   ├── models/            # Pydantic models
│   │   └── schemas.py
│   ├── main.py           # FastAPI application
│   └── dashboard.py      # Streamlit dashboard
├── uploads/              # Temporary file storage
├── Dockerfile           # API Docker image
├── Dockerfile.streamlit # Dashboard Docker image
├── docker-compose.yml   # Multi-container setup
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nidhivaishnav/AI-Resume-Analyzer-Job-Matching-Platform.git
   cd AI-Resume-Analyzer-Job-Matching-Platform
   ```

2. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key for LLM features
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the applications**
   - Dashboard: http://localhost:8501
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nidhivaishnav/AI-Resume-Analyzer-Job-Matching-Platform.git
   cd AI-Resume-Analyzer-Job-Matching-Platform
   ```

2. **Run setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Start the API server**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Start the dashboard (in a new terminal)**
   ```bash
   source venv/bin/activate
   streamlit run app/dashboard.py
   ```

## 📚 API Endpoints

### 1. Analyze Resume
```http
POST /api/analyze-resume
Content-Type: multipart/form-data

Parameters:
- file: PDF file (multipart/form-data)

Response:
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "extracted_skills": ["python", "machine learning", "docker"],
  "key_phrases": ["data analysis", "project management"],
  "text_preview": "Resume text..."
}
```

### 2. Match Job
```http
POST /api/match-job
Content-Type: multipart/form-data

Parameters:
- file: PDF file
- job_description: Job description text

Response:
{
  "overall_score": 75.5,
  "tfidf_score": 68.2,
  "semantic_score": 82.1,
  "skill_match_score": 76.0,
  "matching_skills": ["python", "docker"],
  "missing_skills": ["kubernetes", "aws"],
  "total_job_skills": 5,
  "matched_skills_count": 3
}
```

### 3. Get AI Feedback
```http
POST /api/get-feedback
Content-Type: multipart/form-data

Parameters:
- file: PDF file
- job_description: Job description text

Response:
{
  "resume_feedback": "Detailed AI-generated feedback...",
  "skill_suggestions": "Learning path recommendations...",
  "match_result": { ... }
}
```

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **NLP**: spaCy (en_core_web_sm)
- **ML**: scikit-learn (TF-IDF), Sentence Transformers
- **LLM**: LangChain + OpenAI GPT-3.5
- **PDF Processing**: PyPDF2, pdfplumber
- **Containerization**: Docker, docker-compose

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for LLM features
API_HOST=0.0.0.0
API_PORT=8000
DASHBOARD_PORT=8501
```

**Note**: The platform works without an OpenAI API key, but AI-powered feedback will be limited to basic suggestions.

## 📊 Usage Examples

### Using the Dashboard

1. Navigate to http://localhost:8501
2. Choose a feature from the sidebar:
   - **Resume Analysis**: Upload a resume to extract skills and information
   - **Job Matching**: Upload resume and job description to get match score
   - **AI Feedback**: Get personalized improvement suggestions

### Using the API

```python
import requests

# Analyze resume
with open('resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/analyze-resume',
        files={'file': f}
    )
    print(response.json())

# Match with job
with open('resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/match-job',
        files={'file': f},
        data={'job_description': 'Looking for Python developer with ML experience...'}
    )
    print(response.json())
```

## 🧪 Testing

The platform includes basic validation. To test manually:

1. **Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **API Documentation**
   Visit http://localhost:8000/docs for interactive API testing

## 🔒 Security

- File uploads are validated (PDF only)
- Uploaded files are automatically cleaned up after processing
- API keys should be stored in environment variables
- CORS is configured for security

## 📈 Future Enhancements

- [ ] Support for multiple resume formats (DOCX, TXT)
- [ ] Batch processing for multiple resumes
- [ ] Advanced analytics and reporting
- [ ] User authentication and profile management
- [ ] Resume template suggestions
- [ ] Interview question generation
- [ ] ATS (Applicant Tracking System) optimization tips

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- Nidhi Vaishnav

## 🙏 Acknowledgments

- spaCy for NLP capabilities
- Sentence Transformers for semantic matching
- LangChain for LLM integration
- FastAPI and Streamlit for excellent frameworks
