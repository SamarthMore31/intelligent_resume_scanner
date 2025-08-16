import streamlit as st
import pandas as pd
from utils.pdf_reader import read_pdf
from parser.resume_parser import ResumeParser
from ranker.candidate_ranker import CandidateRanker
from utils.skill_extractor import extract_skills_from_jd
import tempfile
import os
import re

st.set_page_config(layout="wide")
st.title("👨‍💼 Intelligent Resume Scanner")

st.sidebar.header("Instructions")
st.sidebar.info(
    "1. Provide the Job Description (JD).\n"
    "2. Upload one or more candidate resumes.\n"
    "3. Click 'Rank Candidates' to see a detailed analysis, including extracted work experience and education."
)

# --- Job Description Input ---
st.header("1. Provide the Job Description")
input_method = st.radio("Choose JD input method:", ("Upload PDF", "Paste Text"), horizontal=True)
jd_text = ""
if input_method == "Paste Text":
    jd_text = st.text_area("Paste the Job Description text here", height=250)
else:
    jd_upload = st.file_uploader("Upload Job Description (PDF only)", type="pdf")
    if jd_upload:
        with st.spinner("Reading Job Description PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                tmpfile.write(jd_upload.getvalue())
                jd_text = read_pdf(tmpfile.name)
            os.remove(tmpfile.name)

# --- Resume Input ---
st.header("2. Upload Resumes")
uploaded_files = st.file_uploader("Upload candidate resumes here (PDFs only)", type="pdf", accept_multiple_files=True)

# --- Analysis Button ---
st.header("3. Analyze")
if st.button("Rank Candidates"):
    if not jd_text.strip():
        st.error("The Job Description is empty. Please provide valid text.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing... This may take a moment. ⏳"):
            try:
                jd_skills, skill_weights = extract_skills_from_jd(jd_text)
                
                if not jd_skills:
                    st.error("Error: Could not extract any skills from the Job Description.")
                    st.warning("This happens when the JD text doesn't contain any relevant keywords.")
                    st.stop()

                candidate_data = []
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                        tmpfile.write(uploaded_file.getvalue())
                        resume_text = read_pdf(tmpfile.name)
                    os.remove(tmpfile.name)
                    
                    if resume_text:
                        parser = ResumeParser(resume_text)
                        details = parser.get_details()
                        candidate_data.append({**details, 'filename': uploaded_file.name})

                ranker = CandidateRanker(candidate_data, skill_weights, jd_text)
                ranked_candidates = ranker.get_ranked_candidates()

                st.success("Analysis Complete! 🎉")
                
                # --- Store results in session state for display ---
                st.session_state['ranked_candidates'] = ranked_candidates

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.exception(e)

# --- Display Results ---
if 'ranked_candidates' in st.session_state:
    st.header("Analysis Results")
    
    # Iterate through each ranked candidate and display their details in an expander
    for i, candidate in enumerate(st.session_state['ranked_candidates']):
        rank = i + 1
        name = candidate.get('name', 'N/A')
        final_score = round(candidate.get('final_score', 0))

        with st.expander(f"**Rank {rank}: {name}** (Final Score: {final_score})"):
            st.subheader("Scores")
            col1, col2, col3 = st.columns(3)
            col1.metric("Final Score", round(candidate.get('final_score', 0)))
            col2.metric("Keyword Score", round(candidate.get('keyword_score', 0)))
            col3.metric("Semantic Score", f"{round(candidate.get('semantic_score', 0))}%")
            
            st.subheader("Matched Skills")
            matched_skills = candidate.get('matched_skills', [])
            st.write(", ".join(matched_skills) if matched_skills else "None")

            # --- NEW: Display Extracted Work Experience ---
            st.subheader("Extracted Work Experience")
            experience = candidate.get('experience', [])
            if experience:
                for job in experience:
                    st.markdown(f"- **{job.get('title', 'N/A')}** at {job.get('company', 'N/A')}")
            else:
                st.write("No work experience found.")

            # --- NEW: Display Extracted Education ---
            st.subheader("Extracted Education")
            education = candidate.get('education', [])
            if education:
                for edu in education:
                    st.markdown(f"- **{edu.get('degree', 'N/A')}**, {edu.get('university', 'N/A')}")
            else:
                st.write("No education details found.")
            
            st.info(f"Source file: {candidate.get('filename', 'N/A')}")