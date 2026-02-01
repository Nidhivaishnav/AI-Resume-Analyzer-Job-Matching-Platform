"""
Basic tests for core functionality
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.skill_extractor import SkillExtractor
from app.core.job_matcher import JobMatcher


def test_skill_extraction():
    """Test skill extraction from text"""
    print("Testing skill extraction...")
    
    extractor = SkillExtractor()
    
    text = """
    Experienced Software Engineer with expertise in Python, JavaScript, and React.
    Strong background in machine learning, Docker, and AWS cloud services.
    Proficient in SQL, MongoDB, and RESTful API development.
    """
    
    skills = extractor.extract_skills(text)
    print(f"  Extracted {len(skills)} skills: {skills}")
    
    assert 'python' in skills, "Should extract Python"
    assert 'javascript' in skills, "Should extract JavaScript"
    assert 'react' in skills, "Should extract React"
    assert 'machine learning' in skills, "Should extract machine learning"
    
    print("  ✓ Skill extraction test passed!")


def test_job_matching():
    """Test job matching functionality"""
    print("\nTesting job matching...")
    
    matcher = JobMatcher()
    
    resume_text = """
    Software Engineer with 5 years of experience.
    Skills: Python, Django, React, PostgreSQL, Docker, AWS.
    Built scalable web applications and REST APIs.
    """
    
    job_description = """
    Looking for a Full Stack Developer.
    Required skills: Python, Django, React, Docker, Kubernetes.
    Experience with cloud platforms (AWS/Azure) preferred.
    """
    
    resume_skills = ['python', 'django', 'react', 'postgresql', 'docker', 'aws']
    job_skills = ['python', 'django', 'react', 'docker', 'kubernetes']
    
    result = matcher.match_resume_to_job(
        resume_text=resume_text,
        job_description=job_description,
        resume_skills=resume_skills,
        job_skills=job_skills
    )
    
    print(f"  Overall score: {result['overall_score']}%")
    print(f"  TF-IDF score: {result['tfidf_score']}%")
    print(f"  Semantic score: {result['semantic_score']}%")
    print(f"  Skill match: {result['skill_match_score']}%")
    print(f"  Matching skills: {result['matching_skills']}")
    print(f"  Missing skills: {result['missing_skills']}")
    
    assert result['overall_score'] > 0, "Should have positive match score"
    assert 'python' in result['matching_skills'], "Should match Python skill"
    assert 'kubernetes' in result['missing_skills'], "Should identify Kubernetes as missing"
    
    print("  ✓ Job matching test passed!")


def test_api_imports():
    """Test that FastAPI app can be imported"""
    print("\nTesting API imports...")
    
    from app.main import app
    
    assert app is not None, "Should import FastAPI app"
    print(f"  API title: {app.title}")
    print("  ✓ API import test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("Running Basic Functionality Tests")
    print("=" * 60)
    
    try:
        test_skill_extraction()
        test_job_matching()
        test_api_imports()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Test failed: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
