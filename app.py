from flask import Flask, render_template, request, make_response, jsonify
import pdfkit
from skills_extractor import extract_skills, extract_experience_years
from job_fetcher import fetch_jobs_simple, match_jobs_to_user

app = Flask(__name__)

# Configure pdfkit
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        data = request.form.to_dict()
        
        # Store data in session or pass to next page
        return render_template('resume_preview.html', data=data)
    
    return render_template('resume_form.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF and return it"""
    data = request.form.to_dict()
    
    # Render template
    rendered = render_template('resume_template.html', **data)
    
    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options={'enable-local-file-access': None}, configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
    
    return response

@app.route('/analyze_and_match', methods=['POST'])
def analyze_and_match():
    """Analyze resume and find matching jobs"""
    data = request.form.to_dict()
    
    # Build resume text from form data
    resume_text = f"""
    {data.get('name', '')}
    {data.get('title', '')}
    {data.get('summary', '')}
    Skills: {data.get('skills', '')}
    Experience: {data.get('experience', '')}
    Education: {data.get('education', '')}
    """
    
    # Extract skills
    extracted_skills = extract_skills(resume_text)
    experience_years = extract_experience_years(resume_text)
    
    # Fetch matching jobs
    jobs = fetch_jobs_simple(extracted_skills, location="India")
    matched_jobs = match_jobs_to_user(extracted_skills, jobs)
    
    # Return results
    return render_template('job_matches.html', 
                          skills=extracted_skills,
                          experience=experience_years,
                          jobs=matched_jobs,
                          user_data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
