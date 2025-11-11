import streamlit as st
import json
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
import PyPDF2
from docx import Document

# Load environment variables
load_dotenv()

# Files for data storage
RESUME_FILE = "resumes.json"
COVER_LETTER_FILE = "cover_letters.json"
RATINGS_FILE = "ratings.json"
PROFILE_FILE = "profile.json"
RESUME_FOLDER = "saved_resumes"

# Create resume folder if it doesn't exist
if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)


def load_profile():
    """Load user profile with links and preferences."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {
        "linkedin": "",
        "github": "",
        "portfolio": "",
        "default_resume_index": None
    }


def save_profile(profile_data):
    """Save user profile to JSON file."""
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile_data, f, indent=2)


def load_resumes():
    """Load all saved resumes from JSON file."""
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "r") as f:
            return json.load(f)
    return []


def save_resume(resume_data, file_bytes=None, file_name=None):
    """Save a new resume to the JSON file and optionally save the file."""
    resumes = load_resumes()

    # If file bytes provided, save the actual file
    if file_bytes and file_name:
        file_path = os.path.join(RESUME_FOLDER, file_name)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        resume_data["file_path"] = file_path
        resume_data["file_name"] = file_name

    resumes.append(resume_data)
    with open(RESUME_FILE, "w") as f:
        json.dump(resumes, f, indent=2)


def load_cover_letters():
    """Load all saved cover letters from JSON file."""
    if os.path.exists(COVER_LETTER_FILE):
        with open(COVER_LETTER_FILE, "r") as f:
            return json.load(f)
    return []


def save_cover_letter(cover_letter_data):
    """Save a cover letter to the JSON file."""
    cover_letters = load_cover_letters()
    cover_letters.append(cover_letter_data)
    with open(COVER_LETTER_FILE, "w") as f:
        json.dump(cover_letters, f, indent=2)


def save_rating(rating_data):
    """Save a cover letter rating for ML training."""
    ratings = []
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, "r") as f:
            ratings = json.load(f)
    ratings.append(rating_data)
    with open(RATINGS_FILE, "w") as f:
        json.dump(ratings, f, indent=2)


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(docx_file):
    """Extract text from uploaded DOCX file."""
    doc = Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def get_latest_resume():
    """Get the most recently saved resume."""
    resumes = load_resumes()
    if resumes:
        return resumes[-1]
    return None


def generate_cover_letter(resume_text, candidate_name, candidate_address, company_name, role_title, why_want_job, job_description="", length="concise", tone="conversational"):
    """Generate a cover letter using Claude Haiku API."""

    # Length instructions
    length_instructions = {
        "concise": "Keep the cover letter concise and focused, between 200-325 words. Be direct and impactful.",
        "standard": "Write a standard-length cover letter, between 325-450 words. Provide more detail while staying focused."
    }

    # Tone instructions
    tone_instructions = {
        "conversational": "Use a warm, conversational tone that is professional but approachable. Write as if speaking to a colleague. Avoid overly formal language while maintaining respect.",
        "professional": "Use a formal, traditional tone. Choose sophisticated vocabulary, avoid contractions, and maintain a serious, business-like demeanor throughout. This is for corporate, finance, law, or government roles.",
        "enthusiastic": "Use an energetic, passionate tone that shows genuine excitement about the role and company. Express enthusiasm naturally without going overboard. Perfect for startups, creative roles, or mission-driven organizations.",
        "confident": "Use a bold, direct tone that emphasizes your unique value proposition. Be assertive about your capabilities without arrogance. Focus on what you bring to the table. Ideal for competitive roles and leadership positions."
    }

    jd_context = ""
    if job_description:
        jd_context = f"\nHere is the job description:\n{job_description}\n"

    prompt = f"""You are a professional cover letter writer. Generate a cover letter following this exact structure:

IMPORTANT INSTRUCTIONS:
- {length_instructions.get(length, length_instructions["concise"])}
- {tone_instructions.get(tone, tone_instructions["conversational"])}

STRUCTURE:

Date: {datetime.now().strftime("%B %d, %Y")}

{candidate_address}


Hiring Manager
{company_name}
[Company Address - use placeholder if unknown]

Dear Hiring Manager:

First Paragraph (Introduction): State why you are writing and include the exact title of the position ({role_title}). If applicable, mention any company connections.

Second Paragraph (Fit with Job): Describe what the candidate offers based on their resume. Provide specific examples of how their qualifications match the job requirements. Use work, classroom, or organizational experiences. Expand on resume details without repeating them verbatim.

Third Paragraph (Fit with Company): Establish synergy between the candidate and {company_name}. Include values, traits, corporate culture, or commitment to diversity that align with the candidate's profile.

Final Paragraph (Closing): Reiterate interest in the position and express interest in an interview. Thank the employer for their time and consideration.

Sincerely,


{candidate_name}

---

Here is the candidate's resume:
{resume_text}
{jd_context}
Here is why the candidate wants this job:
{why_want_job}

Generate the complete cover letter now, following the structure exactly. Apply the specified tone and length requirements. Do not use emojis. Make it specific to this candidate and company."""

    # Initialize client inside function to avoid initialization issues
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


# Streamlit UI
st.set_page_config(page_title="Application Assistant", page_icon="📄", layout="wide")

st.title("Application Assistant")
st.caption("Your AI-powered job application toolkit")

# Load profile
profile = load_profile()

# Sidebar for profile and resume management
with st.sidebar:
    # Section 1: Your Profile (Candidate Info)
    st.header("Your Profile")

    candidate_name = st.text_input(
        "Your Full Name:",
        value=st.session_state.get("candidate_name", "")
    )

    candidate_address = st.text_area(
        "Your Address:",
        value=st.session_state.get("candidate_address", ""),
        height=80,
        help="Auto-filled from saved resumes but you can edit it."
    )

    st.divider()

    # Section 2: Profile Links
    st.subheader("Profile Links")

    # Display saved links
    if profile.get("linkedin") or profile.get("github") or profile.get("portfolio"):
        if profile.get("linkedin"):
            st.markdown(f"[LinkedIn]({profile['linkedin']})")
        if profile.get("github"):
            st.markdown(f"[GitHub]({profile['github']})")
        if profile.get("portfolio"):
            st.markdown(f"[Portfolio]({profile['portfolio']})")
    else:
        st.info("No profile links saved yet.")

    # Edit profile links
    with st.expander("Edit Profile Links", expanded=False):
        linkedin_url = st.text_input("LinkedIn URL:", value=profile.get("linkedin", ""))
        github_url = st.text_input("GitHub URL:", value=profile.get("github", ""))
        portfolio_url = st.text_input("Portfolio URL:", value=profile.get("portfolio", ""))

        if st.button("Save Profile Links", use_container_width=True):
            profile["linkedin"] = linkedin_url
            profile["github"] = github_url
            profile["portfolio"] = portfolio_url
            save_profile(profile)
            st.success("Profile links saved!")
            st.rerun()

    st.divider()

    # Section 3: Resume Management
    st.subheader("Resume Management")

    # Load existing resumes
    saved_resumes = load_resumes()

    if saved_resumes:
        # Quick action: Use Latest Resume
        latest_resume = saved_resumes[-1]
        st.info(f"Latest: {latest_resume['name']}")
        if st.button("Use Latest Resume", use_container_width=True):
            st.session_state["resume_text"] = latest_resume["resume_text"]
            st.session_state["candidate_name"] = latest_resume["name"]
            st.session_state["candidate_address"] = latest_resume["address"]
            st.success("Latest resume loaded!")
            st.rerun()

        st.divider()

        # Full resume selector
        resume_options = ["Enter new resume"] + [f"{r['name']} - {r['date_saved']}" for r in saved_resumes]
        selected_resume = st.selectbox("Or select any resume:", resume_options)

        if selected_resume != "Enter new resume":
            resume_index = resume_options.index(selected_resume) - 1
            selected_resume_data = saved_resumes[resume_index]
            st.session_state["resume_text"] = selected_resume_data["resume_text"]
            st.session_state["candidate_name"] = selected_resume_data["name"]
            st.session_state["candidate_address"] = selected_resume_data["address"]

            # Show download button if file exists
            if selected_resume_data.get("file_path") and os.path.exists(selected_resume_data["file_path"]):
                with open(selected_resume_data["file_path"], "rb") as f:
                    st.download_button(
                        label=f"Download {selected_resume_data.get('file_name', 'Resume')}",
                        data=f.read(),
                        file_name=selected_resume_data.get('file_name', 'resume.pdf'),
                        mime="application/octet-stream",
                        use_container_width=True
                    )
    else:
        st.info("No saved resumes yet. Add your first resume below.")

    # Add/Update Resume section
    with st.expander("Add New Resume", expanded=False):
        upload_option = st.radio("How would you like to provide your resume?", ["Paste text", "Upload file"], horizontal=True)

        if upload_option == "Upload file":
            uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.pdf'):
                        resume_text = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.name.endswith('.docx'):
                        resume_text = extract_text_from_docx(uploaded_file)
                    st.success("Resume uploaded successfully!")
                    st.session_state["resume_text"] = resume_text
                    st.session_state["uploaded_file"] = uploaded_file
                    st.session_state["uploaded_file_name"] = uploaded_file.name
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    resume_text = ""
            else:
                resume_text = st.session_state.get("resume_text", "")
        else:
            resume_text = st.text_area(
                "Your Resume (paste full resume text):",
                value=st.session_state.get("resume_text", ""),
                height=150
            )
            # Clear uploaded file from session if pasting text
            if "uploaded_file" in st.session_state:
                del st.session_state["uploaded_file"]

        # Save resume button
        if st.button("Save Resume", use_container_width=True):
            if not all([candidate_name, candidate_address, resume_text]):
                st.error("Please fill in name, address, and resume text to save.")
            else:
                resume_data = {
                    "name": candidate_name,
                    "address": candidate_address,
                    "resume_text": resume_text,
                    "date_saved": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "file" if "uploaded_file" in st.session_state else "text"
                }

                # Save file if uploaded
                if "uploaded_file" in st.session_state and "uploaded_file_name" in st.session_state:
                    file_obj = st.session_state["uploaded_file"]
                    file_name = st.session_state["uploaded_file_name"]
                    # Generate unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    unique_file_name = f"{timestamp}_{file_name}"
                    save_resume(resume_data, file_obj.getvalue(), unique_file_name)
                else:
                    save_resume(resume_data)

                st.success(f"Resume saved! You now have {len(load_resumes())} saved resume(s).")

    st.divider()

    # Section 4: Cover Letter History
    st.subheader("Cover Letter History")
    saved_cover_letters = load_cover_letters()
    if saved_cover_letters:
        st.caption(f"Total saved: {len(saved_cover_letters)}")
        for i, cl in enumerate(reversed(saved_cover_letters[-5:])):
            with st.expander(f"{cl['company']} - {cl['role']}", expanded=False):
                st.text(cl['cover_letter'][:200] + "...")
                st.caption(f"Created: {cl['date_created']}")
    else:
        st.info("No saved cover letters yet.")

# Main area - Job Details and Cover Letter Generation
st.header("Generate Cover Letter")

# Get resume text from session (populated via sidebar)
resume_text = st.session_state.get("resume_text", "")
candidate_name = st.session_state.get("candidate_name", "")
candidate_address = st.session_state.get("candidate_address", "")

# Show status
if not resume_text:
    st.warning("Please add or select a resume from the sidebar to get started.")
else:
    st.success(f"Using resume for: {candidate_name if candidate_name else 'Unknown'}")

st.divider()

# Job details
st.subheader("Job Details")

company_name = st.text_input("Company Name:")
role_title = st.text_input("Role/Position Title:")

job_description = st.text_area(
    "Job Description (optional but recommended):",
    height=150,
    help="Paste the job description here for better-tailored cover letters."
)

why_want_job = st.text_area(
    "Why do you want this job? (rough notes are fine):",
    height=150,
    help="Be honest and specific. This will be refined into professional cover letter language."
)

st.divider()

# Preferences
st.subheader("Preferences")

col1, col2 = st.columns(2)

with col1:
    length_option = st.radio(
        "Letter Length:",
        ["Concise (200-325 words)", "Standard (325-450 words)"],
        index=0,
        help="Concise is recommended for most applications"
    )

with col2:
    tone_option = st.selectbox(
        "Tone:",
        [
            "Conversational - Warm but professional",
            "Professional - Formal and traditional",
            "Enthusiastic - Energetic and passionate",
            "Confident - Bold and direct"
        ],
        index=0,
        help="Match the tone to the company culture"
    )

# Generate button
if st.button("Generate Cover Letter", type="primary"):
    if not all([candidate_name, candidate_address, resume_text, company_name, role_title, why_want_job]):
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Generating your cover letter..."):
            try:
                # Parse preferences
                length = "concise" if "Concise" in length_option else "standard"
                tone = tone_option.split(" - ")[0].lower()

                # Generate cover letter
                cover_letter = generate_cover_letter(
                    resume_text,
                    candidate_name,
                    candidate_address,
                    company_name,
                    role_title,
                    why_want_job,
                    job_description,
                    length,
                    tone
                )

                # Store in session state for rating
                st.session_state["last_cover_letter"] = cover_letter
                st.session_state["last_generation_data"] = {
                    "company": company_name,
                    "role": role_title,
                    "resume_text": resume_text,
                    "job_description": job_description,
                    "why_want_job": why_want_job
                }

                st.success("Cover letter generated!")

                # Display the cover letter
                st.subheader("Your Cover Letter")
                st.text_area("", value=cover_letter, height=500, key="generated_cl")

                # Action buttons in columns
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.download_button(
                        label="Download Cover Letter",
                        data=cover_letter,
                        file_name=f"cover_letter_{company_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

                with col2:
                    if st.button("Save Cover Letter"):
                        cover_letter_data = {
                            "company": company_name,
                            "role": role_title,
                            "cover_letter": cover_letter,
                            "date_created": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        save_cover_letter(cover_letter_data)
                        st.success("Cover letter saved!")

                # Rating system
                st.divider()
                st.subheader("Rate this cover letter")
                st.caption("Help improve future generations by rating this output")

                rating_col1, rating_col2 = st.columns(2)

                with rating_col1:
                    if st.button("Good", use_container_width=True):
                        rating_data = {
                            "rating": "good",
                            "cover_letter": cover_letter,
                            "resume_text": resume_text,
                            "job_description": job_description,
                            "why_want_job": why_want_job,
                            "company": company_name,
                            "role": role_title,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_rating(rating_data)
                        st.success("Thanks for your feedback!")

                with rating_col2:
                    if st.button("Bad", use_container_width=True):
                        rating_data = {
                            "rating": "bad",
                            "cover_letter": cover_letter,
                            "resume_text": resume_text,
                            "job_description": job_description,
                            "why_want_job": why_want_job,
                            "company": company_name,
                            "role": role_title,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_rating(rating_data)
                        st.info("Thanks for your feedback. We'll use this to improve!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure your ANTHROPIC_API_KEY is set in the .env file.")
