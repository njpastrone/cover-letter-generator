# AI-Powered Application Assistant - Project Documentation

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

AI-Powered Application Assistant is a comprehensive job application toolkit that helps users:
1. Generate professional cover letters with AI
2. Answer application questions intelligently
3. Manage resumes and profile information
4. Track application history (with account)

### Core Workflow
1. **Guest Mode**: Use immediately without signup - generate and download cover letters
2. **Account Mode**: Save profile, resumes, and cover letter history
3. Input company, role, and job description
4. Generate professional cover letter or answer application questions
5. Download in multiple formats (.txt, .docx, .pdf)

## Technical Stack

- **Frontend**: Python 3.x + Streamlit
- **AI Engine**: Anthropic Claude Haiku API (~$0.0008 per letter)
- **Database**: Supabase (PostgreSQL with row-level security)
- **Authentication**: Supabase Auth (email/password + guest mode)
- **File Processing**: PyPDF2 (PDF), python-docx (DOCX), fpdf2 (PDF export)
- **Deployment**: Streamlit Community Cloud

## Features Implemented

### User Experience
- **Home Page**: Feature overview, technical details, and "Get Started" CTA
- **Guest Mode**: Use app immediately without account creation
- **Authentication**: Email/password signup with Supabase
- **First-Time User Guide**: Welcome banner with quick start steps
- **Help Section**: Collapsible sidebar guide always available

### Profile Management (Account Only)
- Save LinkedIn, GitHub, and Portfolio URLs
- Quick access links with copy functionality
- Profile persists across sessions
- Name and address auto-fill from saved resumes

### Resume Management (Account Only)
- Save multiple resumes with metadata
- Upload PDF/DOCX files with automatic text extraction
- "Use Latest Resume" one-click button for fast workflow
- Full resume history with dropdown selector

### Cover Letter Generation
- Claude Haiku AI-powered generation
- Job description context for better tailoring
- Professional format following template
- **Customizable length options:**
  - Concise (200-325 words) - Default, recommended for most applications
  - Standard (325-450 words) - More detailed coverage
- **Customizable tone options:**
  - Conversational - Warm but professional, approachable (Default)
  - Professional - Formal and traditional (best for: corporate, finance, law, government)
  - Enthusiastic - Energetic and passionate (best for: startups, creative roles, mission-driven orgs)
  - Confident - Bold and direct (best for: competitive roles, leadership positions)
- **Resume Highlight**: Emphasize specific experiences from resume
- **Additional Context**: Add general application context
- Download in multiple formats (.txt, .docx, .pdf)
- Save cover letters to history (account only)

### Application Question Answerer
- Generate intelligent answers to application essay questions
- Context-aware: Avoids repeating content from cover letter or previous answers
- Question-specific notes for more authentic responses
- Session tracking to prevent repetition across multiple questions
- "Clear Session" button to start fresh for new applications

### Data Collection & ML Preparation (Account Only)
- Save cover letters for future reference
- Rating system (Good/Bad) for each generation
- All ratings stored in Supabase `ratings` table with full context
- This data can be used to:
  - Train a custom ML model
  - Fine-tune prompts
  - Identify patterns in good vs bad outputs
  - Build a recommendation system

## Prompt Engineering Architecture

The application uses advanced prompt engineering techniques based on Anthropic's best practices (2024-2025):

### XML Tag Structure
The prompt uses XML tags to clearly separate different components:
- `<instructions>` - Contains length, tone, and additional requirements
- `<resume>` - Candidate's resume text
- `<job_description>` - Job posting details (or note if not provided)
- `<candidate_motivation>` - Why they want the job
- `<output_format>` - Cover letter structure template

**Why XML tags?** Claude is specifically trained to recognize XML tags, which:
- Prevents confusion between instructions and content
- Improves accuracy by 20-30%
- Reduces hallucinations and instruction-following errors
- Makes parsing and modifications easier

### System Message
A dedicated system message establishes Claude as an expert cover letter writer with:
- 15 years of experience across all industries
- Core competencies in matching skills, narrative writing, tone adaptation
- Focus on concrete examples and authentic language

**Why system messages?** More effective role-setting than embedding in user message, resulting in more consistent expert-level output.

### Dynamic Instructions
The prompt adapts based on user preferences:
- **Length**: Concise (200-325 words) vs Standard (325-450 words)
- **Tone**: Conversational, Professional, Enthusiastic, or Confident

Each option includes specific guidance on vocabulary, formality, and style appropriate for different industries and company cultures.

## Database Schema (Supabase)

### Tables
- **profiles** - User profile with links, name, address, and preferences (RLS enabled)
- **resumes** - Saved user resumes with metadata (user_id, resume_name, resume_address, resume_text, date_saved)
- **cover_letters** - Generated and saved cover letters (user_id, company, role, cover_letter, date_created)
- **ratings** - Rated cover letters with full context for ML training (user_id, rating, cover_letter, resume_text, job_description, etc.)

### Authentication
- Supabase Auth with email/password
- Row-level security policies ensure users only access their own data
- Guest mode for anonymous usage (no database access)

## Deployment

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set up `.env` file with Supabase and Anthropic credentials
3. Run: `streamlit run app.py`

### Streamlit Community Cloud
1. Push code to GitHub (secrets in `.gitignore`)
2. Deploy on share.streamlit.io
3. Add secrets in Streamlit Cloud settings
4. See `DEPLOYMENT.md` for detailed instructions

## Future Enhancements

- Application tracking dashboard (companies applied to, dates, status)
- Email templates for follow-ups and thank-you notes
- Interview preparation materials and common questions
- Multiple cover letter templates/styles
- Chrome extension for job board integration
- Resume builder/editor
- AI-powered resume optimization suggestions
