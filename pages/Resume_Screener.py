import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
import io
from dotenv import load_dotenv

# 1. Setup & Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the model that worked for you in previous steps
MODEL_NAME = 'gemini-1.5-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# 2. Helper Function to Process the Uploaded PDF
def get_pdf_text(uploaded_file):
    text = ""
    # We use io.BytesIO because the file is in memory, not on disk
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 3. The Page UI
st.title("📄 AI Resume Screener")
st.markdown("### Optimize your resume for Applicant Tracking Systems (ATS)")

# --- Input Section ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf", help="Please upload a standard text-based PDF.")
    
    with col2:
        job_description = st.text_area("Paste Job Description", height=200, placeholder="Copy and paste the job requirements here...")

# --- Analysis Logic ---
if st.button("Analyze Resume"):
    if uploaded_file is not None and job_description:
        
        with st.spinner("Processing your resume..."):
            try:
                # Step 1: Extract Text from the uploaded PDF
                resume_text = get_pdf_text(uploaded_file)
                
                # Step 2: Create the Prompt
                prompt = f"""
                Act as a Senior Technical Recruiter and Resume Expert.
                
                Here is a candidate's resume text:
                {resume_text}
                
                Here is the target job description:
                {job_description}
                
                Please provide a professional evaluation in the following format:
                
                ### 1. Match Score
                [Give a percentage score out of 100 based on keyword matching and relevance]
                
                ### 2. Missing Keywords
                [List critical skills or keywords found in the JD but missing from the resume]
                
                ### 3. Profile Summary
                [A 2-sentence summary of the candidate's fit for this specific role]
                
                ### 4. Improvement Recommendations
                [3-5 bullet points on specific actionable changes to improve the resume]
                """
                
                # Step 3: Get Response from Gemini
                response = model.generate_content(prompt)
                
                # Step 4: Display Results
                st.markdown("---")
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
    else:
        st.warning("⚠️ Please upload a resume AND paste a job description to proceed.")