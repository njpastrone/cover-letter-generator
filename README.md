# Cover Letter Generator

A simple Streamlit application that generates professional cover letters using Claude Haiku AI.

## Features

- Save and reuse resumes
- Upload resumes as PDF or DOCX files
- Auto-populate candidate information from saved resumes
- Edit candidate address before generating
- Add job description context for better-tailored cover letters
- Generate professional cover letters using Claude Haiku AI
- Save generated cover letters for future reference
- Download cover letters as text files
- Rate cover letters (Good/Bad) to build training data for future ML improvements

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Anthropic API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Enter your name and address
2. Upload your resume (PDF/DOCX) or paste resume text
3. Optionally save the resume for future use
4. Enter the company name and role title
5. Paste the job description (optional but recommended)
6. Write a rough explanation of why you want the job
7. Click "Generate Cover Letter"
8. Rate the output (Good/Bad) to help improve future generations
9. Save or download the generated cover letter

## Cost

Using Claude Haiku API costs approximately $0.0008 per cover letter generated (less than a penny).

## File Structure

- `app.py` - Main Streamlit application
- `resumes.json` - Saved resumes (auto-generated)
- `cover_letters.json` - Saved cover letters (auto-generated)
- `ratings.json` - Cover letter ratings for ML training (auto-generated)
- `requirements.txt` - Python dependencies
- `.env` - API key configuration (create from .env.example)
- `CLAUDE.md` - Project rules and cover letter format template
