from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
import re
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
app.config["UPLOAD_FOLDER"] = "uploads"
ALLOWED_EXTENSIONS = {"txt"}

SKILL_GROUPS = {
    "Programming": ["python", "java", "javascript", "typescript", "c++", "c#", "php", "sql"],
    "Web Development": ["html", "css", "react", "node.js", "flask", "django", "api", "rest api"],
    "Data & AI": ["machine learning", "deep learning", "data analysis", "pandas", "numpy", "tensorflow", "pytorch", "artificial intelligence", "ai", "llm"],
    "Tools": ["git", "github", "docker", "aws", "azure", "linux", "excel", "power bi", "tableau"],
    "Soft Skills": ["communication", "leadership", "teamwork", "problem solving", "project management"]
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_skills(text):
    lower = text.lower()
    found = []
    for group, skills in SKILL_GROUPS.items():
        matches = [skill for skill in skills if re.search(r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)", lower)]
        if matches:
            found.append({"group": group, "skills": sorted(set(matches))})
    return found

def analyze_resume(resume_text, job_description):
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    resume_skills = {skill for skills in SKILL_GROUPS.values() for skill in skills if re.search(r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)", resume_lower)}
    job_skills = {skill for skills in SKILL_GROUPS.values() for skill in skills if re.search(r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)", job_lower)}
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    if job_skills:
        score = round((len(matched) / len(job_skills)) * 100)
    else:
        score = 0

    strengths = []
    if matched:
        strengths.append("Resume mentions job-related skills: " + ", ".join(matched[:10]) + ".")
    if re.search(r"\b(project|projects|internship|experience|developed|built|created)\b", resume_lower):
        strengths.append("Resume includes project or experience-related wording.")
    if re.search(r"\b(bachelor|b\.tech|btech|degree|diploma|university|college|education)\b", resume_lower):
        strengths.append("Resume includes education-related information.")
    if not strengths:
        strengths.append("Add clear skills, projects, education, and experience details to make the resume easier to assess.")

    improvements = []
    if missing:
        improvements.append("Job description skills not found in the resume: " + ", ".join(missing[:12]) + ".")
    if len(resume_text.split()) < 100:
        improvements.append("Resume text is short. Add measurable project details, responsibilities, and achievements if applicable.")
    if not re.search(r"\b(project|projects)\b", resume_lower):
        improvements.append("Consider adding a Projects section with your role, tools used, and outcomes.")
    if not re.search(r"\b(experience|internship|employment|worked)\b", resume_lower):
        improvements.append("Add relevant work, internship, volunteering, or practical experience if you have it.")
    if not improvements:
        improvements.append("No obvious keyword gaps were detected. Review the resume for accuracy, clarity, and measurable results.")

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "skills": extract_skills(resume_text),
        "strengths": strengths,
        "improvements": improvements,
        "word_count": len(resume_text.split())
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    resume_text = ""
    job_description = ""
    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        resume_text = request.form.get("resume_text", "").strip()
        uploaded = request.files.get("resume_file")

        if uploaded and uploaded.filename:
            if not allowed_file(uploaded.filename):
                error = "For this basic version, upload a .txt resume file. PDF/DOCX support is not included."
            else:
                safe_name = secure_filename(uploaded.filename)
                content = uploaded.read().decode("utf-8", errors="ignore")
                resume_text = content.strip()

        if not error and not resume_text:
            error = "Please paste resume text or upload a .txt file."
        elif not error and not job_description:
            error = "Please enter the job description."
        elif not error:
            result = analyze_resume(resume_text, job_description)

    return render_template("index.html", result=result, error=error, resume_text=resume_text, job_description=job_description)

@app.errorhandler(413)
def too_large(_error):
    return "File too large. Maximum upload size is 5 MB.", 413

if __name__ == "__main__":
    app.run(debug=True)
