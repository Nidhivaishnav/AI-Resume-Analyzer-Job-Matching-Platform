"""
Streamlit Dashboard for AI Resume Analyzer
Provides a user-friendly interface for resume analysis and job matching
"""
import streamlit as st
import requests
from pathlib import Path
import json

# API Configuration
API_URL = "http://localhost:8000"

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .high-score {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .medium-score {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .low-score {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎯 AI Resume Analyzer & Job Matching Platform</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Select a feature:",
    ["Resume Analysis", "Job Matching", "AI Feedback"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This platform uses:
- **FastAPI** for backend
- **spaCy** for NLP
- **Sentence Transformers** for semantic matching
- **LangChain** for AI feedback
""")


def analyze_resume(uploaded_file):
    """Call API to analyze resume"""
    try:
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/api/analyze-resume", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the FastAPI server is running on http://localhost:8000")
        return None


def match_job(uploaded_file, job_description):
    """Call API to match resume with job"""
    try:
        files = {"file": uploaded_file}
        data = {"job_description": job_description}
        response = requests.post(f"{API_URL}/api/match-job", files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the FastAPI server is running on http://localhost:8000")
        return None


def get_feedback(uploaded_file, job_description):
    """Call API to get AI feedback"""
    try:
        files = {"file": uploaded_file}
        data = {"job_description": job_description}
        response = requests.post(f"{API_URL}/api/get-feedback", files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.info("Make sure the FastAPI server is running on http://localhost:8000")
        return None


# Page: Resume Analysis
if page == "Resume Analysis":
    st.header("📄 Resume Analysis")
    st.write("Upload your resume to extract skills, contact information, and key insights.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Analyze Resume", type="primary"):
            with st.spinner("Analyzing resume..."):
                result = analyze_resume(uploaded_file)
                
                if result:
                    st.success("✅ Analysis Complete!")
                    
                    # Contact Information
                    st.subheader("👤 Contact Information")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Name", result.get('name', 'N/A'))
                    with col2:
                        st.metric("Email", result.get('email', 'N/A'))
                    with col3:
                        st.metric("Phone", result.get('phone', 'N/A'))
                    
                    # Extracted Skills
                    st.subheader("🎯 Extracted Skills")
                    if result.get('extracted_skills'):
                        skills_cols = st.columns(4)
                        for idx, skill in enumerate(result['extracted_skills']):
                            with skills_cols[idx % 4]:
                                st.button(skill, disabled=True, use_container_width=True)
                    else:
                        st.info("No skills extracted")
                    
                    # Key Phrases
                    st.subheader("💡 Key Phrases")
                    if result.get('key_phrases'):
                        for phrase in result['key_phrases'][:10]:
                            st.write(f"• {phrase}")
                    
                    # Text Preview
                    st.subheader("📝 Resume Text Preview")
                    st.text_area("Preview", result.get('text_preview', ''), height=200)


# Page: Job Matching
elif page == "Job Matching":
    st.header("🎯 Job Matching")
    st.write("Match your resume against a job description and get a compatibility score.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'], key="match")
    
    job_description = st.text_area(
        "Paste Job Description",
        height=200,
        placeholder="Paste the complete job description here..."
    )
    
    if uploaded_file is not None and job_description:
        if st.button("Calculate Match", type="primary"):
            with st.spinner("Calculating match score..."):
                result = match_job(uploaded_file, job_description)
                
                if result:
                    st.success("✅ Match Analysis Complete!")
                    
                    # Overall Score
                    score = result['overall_score']
                    score_class = "high-score" if score >= 70 else "medium-score" if score >= 50 else "low-score"
                    
                    st.markdown(f"""
                    <div class="score-box {score_class}">
                        <h2 style="margin: 0;">Overall Match Score: {score}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed Scores
                    st.subheader("📊 Detailed Scores")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("TF-IDF Score", f"{result['tfidf_score']}%")
                    with col2:
                        st.metric("Semantic Score", f"{result['semantic_score']}%")
                    with col3:
                        st.metric("Skill Match", f"{result['skill_match_score']}%")
                    
                    # Skills Analysis
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("✅ Matching Skills")
                        st.metric("Count", f"{result['matched_skills_count']} / {result['total_job_skills']}")
                        if result.get('matching_skills'):
                            for skill in result['matching_skills']:
                                st.success(f"✓ {skill}")
                        else:
                            st.info("No matching skills found")
                    
                    with col2:
                        st.subheader("❌ Missing Skills")
                        if result.get('missing_skills'):
                            for skill in result['missing_skills']:
                                st.error(f"✗ {skill}")
                        else:
                            st.success("No missing skills!")


# Page: AI Feedback
elif page == "AI Feedback":
    st.header("🤖 AI-Powered Feedback")
    st.write("Get personalized feedback and suggestions to improve your resume.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'], key="feedback")
    
    job_description = st.text_area(
        "Paste Job Description",
        height=200,
        placeholder="Paste the complete job description here..."
    )
    
    if uploaded_file is not None and job_description:
        if st.button("Get AI Feedback", type="primary"):
            with st.spinner("Generating AI feedback... This may take a moment."):
                result = get_feedback(uploaded_file, job_description)
                
                if result:
                    st.success("✅ Feedback Generated!")
                    
                    # Match Score
                    match = result['match_result']
                    score = match['overall_score']
                    score_class = "high-score" if score >= 70 else "medium-score" if score >= 50 else "low-score"
                    
                    st.markdown(f"""
                    <div class="score-box {score_class}">
                        <h3 style="margin: 0;">Match Score: {score}%</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Resume Feedback
                    st.subheader("📝 Resume Feedback")
                    st.markdown(result['resume_feedback'])
                    
                    # Skill Suggestions
                    st.subheader("🎓 Skill Development Suggestions")
                    st.markdown(result['skill_suggestions'])
                    
                    # Missing Skills
                    if match.get('missing_skills'):
                        st.subheader("❌ Skills to Acquire")
                        for skill in match['missing_skills']:
                            st.warning(f"• {skill}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>AI Resume Analyzer & Job Matching Platform v1.0.0</p>
        <p>Powered by FastAPI, spaCy, Sentence Transformers, and LangChain</p>
    </div>
""", unsafe_allow_html=True)
