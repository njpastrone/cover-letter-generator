# Cover Letter Generator - Project Documentation

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

A simple Streamlit application that generates professional cover letters based on:
1. User's resume (can save and reuse resumes, upload PDF/DOCX files)
2. Company and role name
3. Job description (optional but recommended)
4. User's reason for wanting the job

## Technical Stack

- Python 3.x
- Streamlit (front-end framework)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- Local JSON file storage for data persistence
- Claude Haiku API for cover letter generation (cost-effective at ~$0.0008 per letter)

## Features Implemented

### Core Features
- Resume management (save, load, reuse)
- PDF/DOCX resume upload support
- Cover letter generation with Claude Haiku
- Job description context for better tailoring
- Download generated cover letters

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

- `resumes.json` - Saved user resumes with metadata
- `cover_letters.json` - All generated and saved cover letters
- `ratings.json` - Rated cover letters with full context for ML training
