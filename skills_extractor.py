import spacy
import re

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Common skills database (you can expand this)
SKILLS_DATABASE = {
    'python', 'java', 'javascript', 'html', 'css', 'flask', 'django',
    'react', 'angular', 'node.js', 'sql', 'mongodb', 'postgresql',
    'machine learning', 'data analysis', 'excel', 'powerpoint',
    'communication', 'teamwork', 'leadership', 'problem solving',
    'project management', 'agile', 'scrum', 'git', 'docker'
}

def extract_skills(resume_text):
    """
    Extract skills from resume text
    
    Args:
        resume_text (str): The text content of the resume
    
    Returns:
        set: Set of extracted skills
    """
    # Convert to lowercase for matching
    text_lower = resume_text.lower()
    
    # Find matching skills
    found_skills = set()
    for skill in SKILLS_DATABASE:
        if skill in text_lower:
            found_skills.add(skill.title())
    
    return found_skills

def extract_experience_years(resume_text):
    """
    Extract years of experience from resume
    
    Args:
        resume_text (str): The text content of the resume
    
    Returns:
        int: Estimated years of experience
    """
    # Look for patterns like "3 years", "5+ years", etc.
    pattern = r'(\d+)\s*\+?\s*years?'
    matches = re.findall(pattern, resume_text.lower())
    
    if matches:
        return max([int(year) for year in matches])
    return 0

def extract_job_titles(resume_text):
    """
    Extract job titles from resume using NLP
    
    Args:
        resume_text (str): The text content of the resume
    
    Returns:
        list: List of job titles found
    """
    doc = nlp(resume_text)
    
    # Common job title keywords
    job_keywords = ['developer', 'engineer', 'manager', 'analyst', 
                   'designer', 'consultant', 'specialist', 'coordinator']
    
    job_titles = []
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "WORK_OF_ART":
            for keyword in job_keywords:
                if keyword in ent.text.lower():
                    job_titles.append(ent.text)
    
    return job_titles

# Test function
if __name__ == "__main__":
    test_text = """
    Software Developer with 3 years of experience in Python, Flask, and JavaScript.
    Strong skills in Machine Learning and Data Analysis.
    """
    
    print("Skills:", extract_skills(test_text))
    print("Experience:", extract_experience_years(test_text), "years")
    print("Job Titles:", extract_job_titles(test_text))
