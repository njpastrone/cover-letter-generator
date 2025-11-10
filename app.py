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


def load_resumes():
    """Load all saved resumes from JSON file."""
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "r") as f:
            return json.load(f)
    return []


def save_resume(resume_data):
    """Save a new resume to the JSON file."""
    resumes = load_resumes()
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


def generate_cover_letter(resume_text, candidate_name, candidate_address, company_name, role_title, why_want_job, job_description=""):
    """Generate a cover letter using Claude Haiku API."""

    jd_context = ""
    if job_description:
        jd_context = f"\nHere is the job description:\n{job_description}\n"

    prompt = f"""You are a professional cover letter writer. Generate a cover letter following this exact structure:

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

Generate the complete cover letter now, following the structure exactly. Write in a professional, genuine tone. Do not use emojis. Make it specific to this candidate and company."""

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
st.title("Cover Letter Generator")

# Sidebar for resume management
with st.sidebar:
    st.header("Resume Management")

    # Load existing resumes
    saved_resumes = load_resumes()

    if saved_resumes:
        resume_options = ["Enter new resume"] + [f"{r['name']} - {r['date_saved']}" for r in saved_resumes]
        selected_resume = st.selectbox("Select a resume:", resume_options)

        if selected_resume != "Enter new resume":
            # Use selected resume
            resume_index = resume_options.index(selected_resume) - 1
            selected_resume_data = saved_resumes[resume_index]
            st.session_state["resume_text"] = selected_resume_data["resume_text"]
            st.session_state["candidate_name"] = selected_resume_data["name"]
            st.session_state["candidate_address"] = selected_resume_data["address"]
    else:
        st.info("No saved resumes yet. Enter your first resume below.")

    st.divider()
    st.header("Saved Cover Letters")
    saved_cover_letters = load_cover_letters()
    if saved_cover_letters:
        st.write(f"Total saved: {len(saved_cover_letters)}")
        for i, cl in enumerate(reversed(saved_cover_letters[-5:])):
            with st.expander(f"{cl['company']} - {cl['role']}"):
                st.text(cl['cover_letter'][:200] + "...")
                st.caption(f"Created: {cl['date_created']}")
    else:
        st.info("No saved cover letters yet.")

# Main form
st.header("Generate Cover Letter")

# Candidate information
candidate_name = st.text_input(
    "Your Full Name:",
    value=st.session_state.get("candidate_name", "")
)

candidate_address = st.text_area(
    "Your Address (editable):",
    value=st.session_state.get("candidate_address", ""),
    height=100,
    help="This will be extracted from your resume but you can edit it."
)

# Resume input with file upload option
st.subheader("Resume")
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
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            resume_text = ""
    else:
        resume_text = st.session_state.get("resume_text", "")
else:
    resume_text = st.text_area(
        "Your Resume (paste full resume text):",
        value=st.session_state.get("resume_text", ""),
        height=200
    )

save_resume_checkbox = st.checkbox("Save this resume for future use")

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

# Generate button
if st.button("Generate Cover Letter", type="primary"):
    if not all([candidate_name, candidate_address, resume_text, company_name, role_title, why_want_job]):
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Generating your cover letter..."):
            try:
                # Save resume if requested
                if save_resume_checkbox:
                    resume_data = {
                        "name": candidate_name,
                        "address": candidate_address,
                        "resume_text": resume_text,
                        "date_saved": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    save_resume(resume_data)
                    st.success("Resume saved!")

                # Generate cover letter
                cover_letter = generate_cover_letter(
                    resume_text,
                    candidate_name,
                    candidate_address,
                    company_name,
                    role_title,
                    why_want_job,
                    job_description
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
