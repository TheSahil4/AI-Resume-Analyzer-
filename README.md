# ResumeIQ — Simple AI Resume Analyzer (Python + Flask)

A beginner-friendly local web app with a modern dark UI. It compares resume text with a job description, identifies matching/missing skills, and gives practical suggestions.

## Important honesty note
This starter uses **rule-based keyword matching**, not a real generative AI model. It works locally without API keys and is easy to understand/edit in VS Code. PDF/DOCX extraction and a hosted AI model are not included in this basic version.

## Requirements
- Python 3.10+
- VS Code
- VS Code Live Server is not used for this project: Flask serves the dynamic page itself.

## Run on Windows / VS Code
1. Extract the ZIP and open the `simple_ai_resume_analyzer` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
4. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run this for the current terminal only:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open the address printed in terminal, usually `http://127.0.0.1:5000`.

## How to use
- Paste resume text into the first box or upload a `.txt` resume.
- Paste the target job description.
- Click **Analyze resume**.
- Review the score, matching skills, gaps, strengths, and suggestions.

## Project structure
- `app.py` — Flask routes and analysis logic.
- `templates/index.html` — page layout.
- `static/style.css` — styling and responsive layout.
- `requirements.txt` — Python dependencies.
- `uploads/` — reserved for future file processing.

## Beginner explanation
Flask receives the form data in `app.py`, checks skill keywords against the resume and job description, then sends the result to `index.html` to display it. The score is the percentage of tracked job skills also found in the resume. It is only a rough indicator, not an objective measure of candidate quality.

## Privacy
This version analyzes the submitted text on your own computer. Do not use its score to make automatic hiring decisions. Review results manually.
