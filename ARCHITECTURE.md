# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Resume Analyzer Platform                   │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────┐          ┌────────────────────┐
│  Streamlit UI      │◄────────►│   FastAPI Backend  │
│  (Port 8501)       │   REST   │   (Port 8000)      │
└────────────────────┘   API    └────────────────────┘
         │                               │
         │                               ├──► Resume Parser
         │                               │    (PyPDF2/pdfplumber)
         │                               │
         │                               ├──► Skill Extractor
         │                               │    (spaCy NLP)
         │                               │
         │                               ├──► Job Matcher
         │                               │    (TF-IDF/Transformers)
         │                               │
         │                               └──► LLM Feedback
         │                                    (LangChain/OpenAI)
         │
         └──────────────────────────────────────────────────────┐
                                                                 │
                        ┌────────────────────────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   User Uploads   │
              │   (PDF Resumes)  │
              └──────────────────┘
```

## Component Overview

### 1. Frontend Layer (Streamlit Dashboard)

**File**: `app/dashboard.py`

**Features**:
- Resume Analysis interface
- Job Matching interface  
- AI Feedback interface
- Interactive visualizations
- Real-time results display

**Technology**: Streamlit 1.31.0

### 2. API Layer (FastAPI)

**File**: `app/main.py`

**Endpoints**:
```
POST /api/analyze-resume     - Extract resume information
POST /api/match-job          - Calculate job match score
POST /api/get-feedback       - Get AI-powered feedback
GET  /health                 - Health check
GET  /                       - API information
```

**Technology**: FastAPI 0.109.0, Uvicorn

### 3. Core Business Logic

#### 3.1 Resume Parser (`app/core/resume_parser.py`)

**Responsibilities**:
- Extract text from PDF files
- Parse contact information (email, phone, name)
- Handle multiple PDF formats

**Technologies**:
- PyPDF2 3.0.1 (fallback)
- pdfplumber 0.10.3 (primary)

**Key Methods**:
```python
parse(pdf_path) -> dict
extract_text_from_pdf(pdf_path) -> str
extract_email(text) -> str
extract_phone(text) -> str
extract_name(text) -> str
```

#### 3.2 Skill Extractor (`app/core/skill_extractor.py`)

**Responsibilities**:
- Extract technical skills from text
- Identify key phrases
- Named entity recognition

**Technologies**:
- spaCy 3.7.2 (en_core_web_sm model)
- Pattern matching with 100+ skill patterns

**Skills Database**:
- Programming languages (Python, Java, JavaScript, etc.)
- Web technologies (React, Angular, Django, etc.)
- Databases (SQL, MongoDB, PostgreSQL, etc.)
- Cloud & DevOps (AWS, Docker, Kubernetes, etc.)
- Data Science & ML (TensorFlow, PyTorch, etc.)

**Key Methods**:
```python
extract_skills(text) -> List[str]
extract_entities(text) -> dict
get_key_phrases(text, top_n) -> List[str]
```

#### 3.3 Job Matcher (`app/core/job_matcher.py`)

**Responsibilities**:
- Calculate similarity between resume and job description
- Multiple matching algorithms
- Skill gap analysis

**Technologies**:
- scikit-learn 1.4.0 (TF-IDF, cosine similarity)
- Sentence Transformers 2.3.1 (semantic embeddings)

**Matching Algorithms**:

1. **TF-IDF Matching** (30% weight)
   - Text-based similarity
   - Fast and efficient
   - Good for keyword matching

2. **Semantic Matching** (40% weight)
   - Sentence Transformers (all-MiniLM-L6-v2)
   - Captures meaning and context
   - Advanced semantic understanding

3. **Skill-based Matching** (30% weight)
   - Direct skill comparison
   - Identifies gaps
   - Precise matching

**Key Methods**:
```python
match_resume_to_job(...) -> dict
calculate_tfidf_similarity(...) -> float
calculate_semantic_similarity(...) -> float
rank_candidates(...) -> List[dict]
```

#### 3.4 LLM Feedback Generator (`app/core/llm_feedback.py`)

**Responsibilities**:
- Generate personalized resume feedback
- Provide skill learning recommendations
- Career development guidance

**Technologies**:
- LangChain Core 0.1.16
- LangChain OpenAI 0.0.5
- OpenAI GPT-3.5-turbo

**Features**:
- Graceful degradation (works without API key)
- Basic feedback as fallback
- Customizable prompts

**Key Methods**:
```python
generate_resume_feedback(...) -> str
suggest_missing_skills(...) -> str
```

### 4. Data Models

**File**: `app/models/schemas.py`

**Models**:
```python
JobDescription          - Input model
ResumeAnalysisResponse - Resume analysis output
MatchResult            - Job matching output
FeedbackResponse       - AI feedback output
```

**Technology**: Pydantic 2.5.3

## Data Flow

### Resume Analysis Flow

```
1. User uploads PDF → Dashboard
2. Dashboard sends to API → /api/analyze-resume
3. API saves file → uploads/
4. ResumeParser extracts text
5. SkillExtractor identifies skills
6. Return structured response
7. Clean up uploaded file
8. Display results in Dashboard
```

### Job Matching Flow

```
1. User uploads resume + job description → Dashboard
2. Dashboard sends to API → /api/match-job
3. ResumeParser extracts resume text
4. SkillExtractor extracts skills from both texts
5. JobMatcher calculates:
   - TF-IDF similarity score
   - Semantic similarity score
   - Skill match percentage
6. Combine scores (weighted average)
7. Identify matching/missing skills
8. Return match results
9. Display scores and gaps in Dashboard
```

### AI Feedback Flow

```
1. User requests feedback → Dashboard
2. Dashboard sends to API → /api/get-feedback
3. Parse resume and extract skills
4. Calculate match score
5. FeedbackGenerator calls LLM:
   - If API key available: Use OpenAI GPT-3.5
   - Otherwise: Use basic feedback template
6. Generate:
   - Resume quality assessment
   - Improvement suggestions
   - Skill learning plan
7. Return comprehensive feedback
8. Display in Dashboard
```

## Deployment Options

### Option 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Terminal 1: Start API
uvicorn app.main:app --reload

# Terminal 2: Start Dashboard
streamlit run app/dashboard.py
```

### Option 2: Docker Compose

```bash
docker-compose up --build
```

**Services**:
- `api`: FastAPI backend (port 8000)
- `dashboard`: Streamlit frontend (port 8501)

**Volumes**:
- `./uploads:/app/uploads` - Persistent file storage

**Environment**:
- `OPENAI_API_KEY` - Optional, for LLM features

## Security Considerations

1. **File Validation**
   - Only PDF files accepted
   - File size limits enforced
   - Automatic cleanup after processing

2. **CORS Configuration**
   - Configured for cross-origin requests
   - Customizable allowed origins

3. **API Key Management**
   - Environment variables only
   - Never committed to repository
   - Optional (graceful fallback)

4. **Data Privacy**
   - Files deleted after processing
   - No persistent storage of resume data
   - Uploads directory in .gitignore

## Performance Characteristics

### Speed

- **Resume Parsing**: ~0.5-2 seconds
- **Skill Extraction**: ~0.1-0.5 seconds
- **Job Matching**: ~1-3 seconds
- **AI Feedback** (with LLM): ~5-30 seconds
- **AI Feedback** (without LLM): ~0.1 seconds

### Resource Usage

- **Memory**: ~500MB-1GB (includes ML models)
- **Disk**: ~2GB (models and dependencies)
- **CPU**: Moderate (spaCy NLP processing)
- **Network**: Minimal (only for LLM API calls)

### Scalability

- Stateless API (horizontally scalable)
- No database required
- Can handle concurrent requests
- Docker-ready for cloud deployment

## Future Enhancements

### Planned Features

1. **Multi-format Support**
   - DOCX resumes
   - Text files
   - LinkedIn profiles

2. **Advanced Analytics**
   - Resume scoring algorithms
   - Industry-specific matching
   - Salary predictions

3. **User Management**
   - User accounts
   - Resume history
   - Saved job matches

4. **Batch Processing**
   - Upload multiple resumes
   - Compare candidates
   - Ranking system

5. **Enhanced AI**
   - Interview question generation
   - Cover letter assistance
   - ATS optimization

6. **Integration**
   - LinkedIn integration
   - Job board APIs
   - Email notifications

## Technology Stack Summary

| Layer           | Technology              | Version  | Purpose                    |
|-----------------|-------------------------|----------|----------------------------|
| Frontend        | Streamlit               | 1.31.0   | User interface             |
| Backend API     | FastAPI                 | 0.109.0  | REST API                   |
| Web Server      | Uvicorn                 | 0.27.0   | ASGI server                |
| PDF Parsing     | pdfplumber              | 0.10.3   | Extract PDF text           |
| PDF Fallback    | PyPDF2                  | 3.0.1    | Backup PDF parser          |
| NLP             | spaCy                   | 3.7.2    | Text analysis              |
| ML Matching     | scikit-learn            | 1.4.0    | TF-IDF, cosine similarity  |
| Semantic Match  | sentence-transformers   | 2.3.1    | Embeddings                 |
| LLM Framework   | langchain-core          | 0.1.16   | LLM orchestration          |
| LLM Provider    | langchain-openai        | 0.0.5    | OpenAI integration         |
| Validation      | Pydantic                | 2.5.3    | Data validation            |
| Containerization| Docker                  | Latest   | Deployment                 |

## Development Workflow

```bash
# 1. Clone repository
git clone https://github.com/Nidhivaishnav/AI-Resume-Analyzer-Job-Matching-Platform.git

# 2. Setup environment
cd AI-Resume-Analyzer-Job-Matching-Platform
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Run tests
python tests/test_basic.py

# 5. Start development
uvicorn app.main:app --reload

# 6. Access API docs
# http://localhost:8000/docs
```

## Monitoring and Health Checks

### API Health Endpoint

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Docker Health Checks

Built-in health checks in docker-compose.yml:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

### Logs

```bash
# Docker logs
docker-compose logs -f

# API logs (development)
# Visible in uvicorn terminal output

# Dashboard logs
# Visible in streamlit terminal output
```
