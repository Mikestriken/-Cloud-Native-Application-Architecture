"""
Streamlit frontend for Resume Job Matcher
"""
import streamlit as st
import requests
import pandas as pd
import io
import PyPDF2
import os
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API endpoint URLs
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")
LOGIN_URL = f"{API_BASE_URL}/token"
REGISTER_URL = f"{API_BASE_URL}/users/"
UPLOAD_RESUME_URL = f"{API_BASE_URL}/upload_resume"
GET_JOBS_URL = f"{API_BASE_URL}/jobs"
GET_JOB_URL = f"{API_BASE_URL}/job"
GET_MATCHES_URL = f"{API_BASE_URL}/match_jobs"

# Set page configuration
st.set_page_config(
    page_title="Resume Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "resume_id" not in st.session_state:
    st.session_state.resume_id = None
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "job_matches" not in st.session_state:
    st.session_state.job_matches = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Upload Resume"  # Default tab

# Helper functions
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def login(email, password):
    """Authenticate user and get access token"""
    try:
        response = requests.post(
            LOGIN_URL,
            data={"username": email, "password": password},
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.logged_in = True
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def register(name, email, password):
    """Register a new user"""
    try:
        response = requests.post(
            REGISTER_URL,
            json={"name": name, "email": email, "password": password}
        )
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        return False

def upload_resume(content):
    """Upload resume and get job matches"""
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    try:
        response = requests.post(
            UPLOAD_RESUME_URL,
            json={"content": content},
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.resume_id = data["resume_id"]
            return data.get("matches", [])
        else:
            logger.error(f"Error uploading resume: {response.status_code} - {response.text}")
            st.error(f"Error uploading resume: {response.text}")
            return []
    except Exception as e:
        logger.exception(f"Exception during resume upload: {str(e)}")
        st.error(f"Upload error: {str(e)}")
        return []

def get_job_matches(resume_id):
    """Get job matches for a resume"""
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    try:
        response = requests.get(
            f"{GET_MATCHES_URL}/{resume_id}",
            headers=headers
        )
        if response.status_code == 200:
            matches = response.json()
            st.session_state.job_matches = matches
            return matches
        else:
            st.error(f"Error getting matches: {response.text}")
            return []
    except Exception as e:
        st.error(f"Match retrieval error: {str(e)}")
        return []

def get_job_details(job_id):
    """Get detailed information about a job"""
    try:
        # Validate job_id before making the request
        if not job_id:
            st.error("Invalid job ID (empty or undefined)")
            return None
            
        url = f"{GET_JOB_URL}/{job_id}"
        logger.info(f"Requesting URL: {url}")
        
        response = requests.get(url)
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting job details: Status {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Exception during job retrieval: {str(e)}")
        st.error(f"Job retrieval error: {str(e)}")
        return None

def logout():
    """Clear session state and log out"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.access_token = None
    st.session_state.resume_id = None
    st.session_state.selected_job = None
    st.session_state.job_matches = []
    st.rerun()

# Sidebar navigation
def render_sidebar():
    """Render the sidebar navigation"""
    st.sidebar.title("Resume Job Matcher")
    
    if st.session_state.logged_in:
        st.sidebar.button("Logout", on_click=logout)
    else:
        st.sidebar.info("Please login or register to continue")

# Login/Register page
def render_auth_page():
    """Render the authentication page"""
    st.title("Welcome to Resume Job Matcher")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login(login_email, login_password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    
    with tab2:
        st.header("Register")
        register_name = st.text_input("Name", key="register_name")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Register"):
            if register_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                if register(register_name, register_email, register_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed. Email might already be registered.")

# Main application page
def render_main_app():
    """Render the main application after login"""
    st.title("Resume Job Matcher")
    
    upload_tab, matches_tab = st.tabs(["Upload Resume", "Job Matches"])
    
    with upload_tab:
        st.header("Upload Your Resume")
        
        # File upload option
        upload_option = st.radio(
            "Choose an option:",
            ["Upload PDF Resume", "Paste Resume Text"]
        )
        
        if upload_option == "Upload PDF Resume":
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file is not None:
                resume_text = extract_text_from_pdf(uploaded_file)
                st.text_area("Extracted Text", resume_text, height=300)
                
                if st.button("Submit Resume"):
                    with st.spinner("Processing resume and finding matches..."):
                        matches = upload_resume(resume_text)
                        
                        logger.info(f"Matches:\n{matches}\n=========================================")
                        if matches:
                            st.success("Resume uploaded successfully! View matches in the Job Matches tab.")
                            st.session_state.job_matches = matches
                            st.session_state.active_tab = "Job Matches"
                            st.rerun()
        else:
            resume_text = st.text_area("Paste your resume text here:", height=300)
            if st.button("Submit Resume"):
                if resume_text:
                    with st.spinner("Processing resume and finding matches..."):
                        matches = upload_resume(resume_text)
                        
                        logger.info(f"Matches:\n{matches}\n=========================================")
                        if matches:
                            st.success("Resume uploaded successfully! View matches in the Job Matches tab.")
                            st.session_state.job_matches = matches
                            st.session_state.active_tab = "Job Matches"
                            st.rerun()
                else:
                    st.warning("Please enter your resume text.")
    
    with matches_tab:
        st.header("Your Job Matches")
        
        if st.session_state.resume_id:
            if st.button("Refresh Matches"):
                with st.spinner("Fetching latest matches..."):
                    matches = get_job_matches(st.session_state.resume_id)
                    if matches:
                        st.success("Matches refreshed!")
        
        if st.session_state.job_matches:
            # Convert matches to DataFrame for easy display
            matches_data = []
            for match in st.session_state.job_matches:
                job_id = match.get("job_id")
                
                # We need to fetch job details separately since they're not included in the match data
                job_details = get_job_details(job_id)
                
                if job_details:
                    matches_data.append({
                        "Job Title": job_details.get("title", ""),
                        "Company": job_details.get("company", ""),
                        "Location": job_details.get("location", ""),
                        "Match Score": f"{match.get('score', 0) * 100:.1f}%",
                        "Job ID": job_id
                    })
                else:
                    # Add basic info if job details couldn't be retrieved
                    matches_data.append({
                        "Job Title": f"Job {job_id}",
                        "Company": "Unknown",
                        "Location": "Unknown",
                        "Match Score": f"{match.get('score', 0) * 100:.1f}%",
                        "Job ID": job_id
                    })
            
            if matches_data:
                df = pd.DataFrame(matches_data)
                
                # Clickable table
                for i, row in df.iterrows():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.button(f"{row['Job Title']} - {row['Company']}", key=f"job_{row['Job ID']}_{i}"):
                            st.session_state.selected_job = row["Job ID"]
                    with col2:
                        st.write(row["Location"])
                    with col3:
                        st.write(row["Match Score"])
                    
                    # Show job details if selected
                    if st.session_state.selected_job == row["Job ID"]:
                        job_details = get_job_details(row["Job ID"])
                        if job_details:
                            with st.expander("Job Details", expanded=True):
                                st.markdown(f"## {job_details['title']}")
                                st.markdown(f"**Company:** {job_details['company']}")
                                st.markdown(f"**Location:** {job_details['location']}")
                                st.markdown("### Job Description")
                                st.markdown(job_details['description'])
            else:
                st.info("No job matches found. Try uploading a different resume.")
        else:
            st.info("Upload your resume to see job matches.")

    # After getting matches
    # logger.info(f"Raw matches structure: {st.session_state.job_matches}")

# Main app flow
def main():
    """Main application entry point"""
    render_sidebar()
    
    if st.session_state.logged_in:
        render_main_app()
    else:
        render_auth_page()

if __name__ == "__main__":
    main() 