# Application Assistant

Your AI-powered job application toolkit. A simple Streamlit application that helps you manage your job application materials and generate professional cover letters using Claude Haiku AI.

## Features

### Profile Management
- Save your LinkedIn, GitHub, and Portfolio URLs for quick access
- "Use Latest Resume" one-click button for fast workflow
- Resume history with easy selection

### Resume Management
- Save and reuse multiple resumes
- Upload resumes as PDF or DOCX files (original files are saved)
- Download saved resume files anytime from sidebar
- Auto-populate candidate information from saved resumes
- Edit candidate address before generating
- Support for both file uploads and pasted text

### Cover Letter Generation
- Generate professional cover letters using Claude Haiku AI
- Add job description context for better-tailored cover letters
- **Customize letter length**: Concise (200-325 words) or Standard (325-450 words)
- **Choose tone style**: Conversational, Professional, Enthusiastic, or Confident
- Match tone to company culture (startup, corporate, creative, etc.)
- Save generated cover letters for future reference
- View cover letter history in sidebar
- Download cover letters as text files

### Continuous Improvement
- Rate cover letters (Good/Bad) to build training data for future ML improvements
- All feedback stored with full context for model training

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

### First Time Setup
1. Save your profile links (LinkedIn, GitHub, Portfolio) in the sidebar
2. Upload or paste your resume and save it for future use

### Generating a Cover Letter
1. Click "Use Latest Resume" for quick access, or select any saved resume
2. Enter the company name and role title
3. Paste the job description (optional but recommended)
4. Write a rough explanation of why you want the job
5. Click "Generate Cover Letter"
6. Rate the output (Good/Bad) to help improve future generations
7. Save or download the generated cover letter

## Cost

Using Claude Haiku API costs approximately $0.0008 per cover letter generated (less than a penny).

## File Structure

- `app.py` - Main Streamlit application
- `profile.json` - User profile with links and preferences (auto-generated)
- `resumes.json` - Resume metadata and text (auto-generated)
- `saved_resumes/` - Folder containing original PDF/DOCX resume files (auto-generated)
- `cover_letters.json` - Saved cover letters (auto-generated)
- `ratings.json` - Cover letter ratings for ML training (auto-generated)
- `requirements.txt` - Python dependencies
- `.env` - API key configuration (create from .env.example)
- `CLAUDE.md` - Project rules and cover letter format template
