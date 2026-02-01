# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup
```bash
git clone https://github.com/Nidhivaishnav/AI-Resume-Analyzer-Job-Matching-Platform.git
cd AI-Resume-Analyzer-Job-Matching-Platform
chmod +x setup.sh && ./setup.sh
```

### Step 2: Run with Docker (Recommended)
```bash
docker-compose up --build
```

**OR** Run Locally:
```bash
# Terminal 1 - API Server
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Dashboard  
source venv/bin/activate
streamlit run app/dashboard.py
```

### Step 3: Access
- 🎨 Dashboard: http://localhost:8501
- 🔌 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 📋 Features at a Glance

| Feature | What it Does | How to Use |
|---------|--------------|------------|
| **Resume Analysis** | Extract skills, contact info | Upload PDF → Click "Analyze" |
| **Job Matching** | Calculate compatibility score | Upload PDF + Job description |
| **AI Feedback** | Get improvement suggestions | Upload PDF + Job description |

## 🎯 API Quick Reference

```python
import requests

# Analyze Resume
with open('resume.pdf', 'rb') as f:
    r = requests.post('http://localhost:8000/api/analyze-resume', files={'file': f})
    print(r.json())

# Match Job
with open('resume.pdf', 'rb') as f:
    r = requests.post('http://localhost:8000/api/match-job', 
                     files={'file': f},
                     data={'job_description': 'Your job description...'})
    print(f"Score: {r.json()['overall_score']}%")
```

## 🔑 Optional: Enable AI Feedback

Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Without API key: Basic feedback still works!

## 📖 Documentation

- 📘 [Full README](README.md) - Complete setup guide
- 📗 [Usage Examples](USAGE.md) - Code examples & troubleshooting  
- 📙 [Architecture](ARCHITECTURE.md) - System design & internals

## ⚡ Tech Stack

**Backend**: FastAPI + Python
**Frontend**: Streamlit  
**NLP**: spaCy (100+ skills)
**ML**: TF-IDF + Sentence Transformers
**AI**: LangChain + OpenAI
**Deploy**: Docker

## 💡 Pro Tips

1. **Best Results**: Use well-formatted PDF resumes
2. **Skill Matching**: Include clear skills section
3. **Job Descriptions**: Paste complete descriptions
4. **Performance**: First run downloads ML models (~1-2GB)
5. **Offline Mode**: Works without OpenAI API key

## 🐛 Common Issues

**Port in use?**
```bash
# Change API port
uvicorn app.main:app --port 8001

# Change Dashboard port  
streamlit run app/dashboard.py --server.port 8502
```

**Missing spaCy model?**
```bash
python -m spacy download en_core_web_sm
```

**Docker issues?**
```bash
docker-compose down
docker-compose up --build
```

## 📊 What You Get

✅ Resume parsing from PDF  
✅ Skill extraction (Python, Java, AWS, etc.)  
✅ Job match score (0-100%)  
✅ Skill gap analysis  
✅ AI-powered feedback  
✅ Learning recommendations  
✅ Interactive dashboard  
✅ REST API  

## 🤝 Support

- 📧 Issues: [GitHub Issues](https://github.com/Nidhivaishnav/AI-Resume-Analyzer-Job-Matching-Platform/issues)
- 📖 Docs: See USAGE.md and ARCHITECTURE.md
- 💬 Questions: Check troubleshooting in USAGE.md

---

**Ready to analyze resumes? Start with `docker-compose up --build`** 🎉
