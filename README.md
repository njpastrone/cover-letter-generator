# AI-Powered Application Assistant

Built by **Nicolo Pastrone**

Your intelligent companion for job applications. A Streamlit web application that helps you generate professional cover letters, answer application questions, and manage your job search materials using AI.

## Features

### Guest Mode
- **No signup required** - Start using immediately
- Generate cover letters and answer application questions
- Download outputs in multiple formats (.txt, .docx, .pdf)
- Perfect for trying out the tool

### Account Mode
- **Save your work** - Create a free account to persist data
- Store multiple resumes with metadata
- Track cover letter history
- Manage profile links (LinkedIn, GitHub, Portfolio)
- Rate cover letters for continuous improvement

### Cover Letter Generation
- **AI-powered** using Claude Haiku API (~$0.0008 per letter)
- **Customizable length**: Concise (200-325 words) or Standard (325-450 words)
- **Multiple tone options**: Conversational, Professional, Enthusiastic, Confident
- Resume highlighting to emphasize specific experiences
- Additional context for special situations
- Professional formatting following industry standards

### Application Question Answerer
- Generate intelligent answers to essay questions
- Context-aware to avoid repetition
- Question-specific notes for authentic responses
- Session tracking across multiple questions
- "Clear Session" for new applications

### User Experience
- **Home page** with feature overview and technical details
- **First-time user guide** with quick start instructions
- **Help section** in sidebar for ongoing reference
- Clean, intuitive interface

## Technical Stack

- **Frontend**: Python + Streamlit
- **AI Engine**: Anthropic's Claude Haiku API
- **Database**: Supabase (PostgreSQL with row-level security)
- **Authentication**: Supabase Auth (email/password + guest mode)
- **File Processing**: PyPDF2, python-docx, fpdf2
- **Deployment**: Streamlit Community Cloud

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with credentials:
```bash
ANTHROPIC_API_KEY=your-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
```

3. Run the app:
```bash
streamlit run app.py
```

### Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Streamlit Community Cloud with Supabase backend.

## Usage

### Quick Start (Guest Mode)
1. Click "Get Started" on home page
2. Select "Continue as Guest"
3. Enter your profile info and resume
4. Fill in job details
5. Generate and download your cover letter

### With Account
1. Create account with email/password
2. Save multiple resumes for quick access
3. Generate cover letters with "Use Latest Resume"
4. View history of saved cover letters
5. Rate outputs to help improve the AI

## Cost

- **Guest mode**: Free to use (you provide your own Anthropic API key if self-hosting)
- **Hosted version**: Approximately $0.0008 per cover letter generated
- **Account storage**: Free on Supabase free tier (500MB database)

## Architecture

### Database Schema (Supabase)
- `profiles` - User profile information (RLS enabled)
- `resumes` - Saved resumes with metadata
- `cover_letters` - Generated cover letter history
- `ratings` - User feedback for ML training

### Authentication
- Email/password via Supabase Auth
- Guest mode for anonymous usage
- Row-level security ensures data isolation

### AI Features
- XML-structured prompts for better Claude comprehension
- System messages for consistent expert-level output
- Dynamic instructions based on user preferences
- Context-aware generation to avoid repetition

## File Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `.env` - API keys and credentials (not committed)
- `CLAUDE.md` - Project documentation and rules
- `DEPLOYMENT.md` - Deployment guide for Streamlit Cloud
- `.streamlit/secrets.toml` - Streamlit Cloud secrets (not committed)

## Future Enhancements

- Application tracking dashboard
- Email templates for follow-ups
- Interview preparation materials
- Multiple cover letter templates
- Chrome extension for job boards
- Resume builder and optimization

## Development

Built with Claude Code, demonstrating modern AI-assisted development workflows. See `CLAUDE.md` for project rules and architecture details.

## License

Personal project by Nicolo Pastrone. Feel free to fork and adapt for your own use.
