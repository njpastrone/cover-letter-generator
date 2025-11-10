# Application Assistant - Project Documentation

## NON-NEGOTIABLE PROJECT RULES

These rules MUST be followed for ALL work on this project:

1. **Always use Python for all development**
2. **Leverage Streamlit for the front-end**
3. **Write beginner-friendly code** - code must be readable and understandable by a beginner Python programmer
4. **Always take the simplest route to solving problems**
5. **The entire app should be "vibe-coder friendly"** - prioritize clarity over cleverness
6. **Make autonomous decisions** - avoid asking for user permissions unless making dangerous changes
7. **Minimize the size of the code base** - keep the project simple with fewer files when possible
8. **Avoid duplicating code**
9. **Refer to markdown files for context consistently**
10. **Do not be afraid to ask the user for questions or clarifications**
11. **NEVER use emojis in the app** - emojis make everything look AI-generated and unprofessional
12. **CONTEXT IS EVERYTHING** - create CLAUDE.md and README.md files in each folder and sub-folder, and update relevant .md files after each code change

## Cover Letter Format

The generated cover letters must follow this structure:

```
Date

Candidate's Address
City, State, Zip Code


Employee's Name (if unavailable, use Hiring Manager or Search Committee)
Employee's Title
Company
Address
City, State, Zip Code

Dear First Name Last Name: (If unknown, put Dear Hiring Manager or Dear Search Committee)

First Paragraph (Introduction): The first paragraph states why you are writing the letter. Include the exact title of the position you are applying for. If you spoke to anyone from the company, include their name and explain what you learned about the company from them.

Second Paragraph (Fit with Job): This paragraph describes what you have to offer the employer as it relates to the job description. Provide examples of how your qualifications and skills match or exceed the job qualifications. Feel free to use work, classroom or student organizational experiences as examples. Remember, you are providing more details to experiences listed on your resume, not repeating them.

Third Paragraph (Fit with Company): This paragraph establishes synergy between you and the company. This can include values, traits, corporate culture, commitment to diversity, etc. This will allow you to show your in-depth knowledge of the employer and how you fit in without restating everything posted on their website.

Final Paragraph (Closing): Reiterate your interest in the position and express your interest in an interview (without stating specific date/time). Conclude by thanking the employer for their time and consideration.

Sincerely,


Candidate's Typed First and Last Name
```

## Project Overview

Application Assistant is a comprehensive job application toolkit that helps users:
1. Manage their professional profile (LinkedIn, GitHub, Portfolio links)
2. Store and reuse resumes (supports paste, PDF, and DOCX uploads)
3. Generate tailored cover letters using AI
4. Track application history and cover letter performance

### Core Workflow
1. Save profile links and latest resume
2. Quick-load latest resume with one click
3. Input company, role, and job description
4. Generate professional cover letter
5. Rate output and save for future reference

## Technical Stack

- Python 3.x
- Streamlit (front-end framework)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- Local JSON file storage for data persistence
- Claude Haiku API for cover letter generation (cost-effective at ~$0.0008 per letter)

## Features Implemented

### Profile Management
- Save LinkedIn, GitHub, and Portfolio URLs
- Quick access links displayed in sidebar
- Profile persists across sessions

### Resume Management
- Save multiple resumes with metadata
- Upload PDF/DOCX files with automatic text extraction
- "Use Latest Resume" one-click button for fast workflow
- Full resume history with dropdown selector

### Cover Letter Generation
- Claude Haiku AI-powered generation
- Job description context for better tailoring
- Professional format following template
- Download generated cover letters
- Save cover letters to history

### Data Collection & ML Preparation
- Save cover letters for future reference
- Rating system (Good/Bad) for each generation
- All ratings stored in `ratings.json` with full context:
  - Generated cover letter
  - Input resume
  - Job description
  - Why they want the job
  - Company and role info
  - Timestamp
- This data can be used to:
  - Train a custom ML model
  - Fine-tune prompts
  - Identify patterns in good vs bad outputs
  - Build a recommendation system

## Data Files

- `profile.json` - User profile with LinkedIn, GitHub, Portfolio URLs and preferences
- `resumes.json` - Saved user resumes with metadata (name, address, text, date)
- `cover_letters.json` - All generated and saved cover letters with metadata
- `ratings.json` - Rated cover letters with full context for ML training

## Future Enhancements

- Application tracking (companies applied to, dates, status)
- Email templates for follow-ups
- Interview preparation materials
- Multiple cover letter templates
- Export to Word/PDF format
- Browser extension for job board integration
