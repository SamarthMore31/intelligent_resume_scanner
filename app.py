import streamlit as st
import pandas as pd
from parser.resume_parser import parse_resume
from ranker.candidate_ranker import CandidateRanker
from utils.skill_extractor import extract_skills_from_jd
import tempfile
import os
from io import StringIO

st.set_page_config(page_title="🚀 Intelligent Resume Scanner", layout="wide")

st.title("🚀 Intelligent Resume Scanner")

st.markdown("""
Upload a **Job Description** (txt or pdf) and multiple **Resumes** (PDF) to get candidates ranked by skill match.  
After upload, click **Analyze** to see results and download the ranking CSV.
""")

jd_file = st.file_uploader("Upload Job Description (txt or pdf)", type=["txt", "pdf"])
resume_files = st.file_uploader("Upload Candidate Resumes (PDF) - You can select multiple", type=["pdf"], accept_multiple_files=True)

analyze_btn = st.button("Analyze")

def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

if analyze_btn:
    if not jd_file:
        st.error("Please upload a Job Description file first.")
    elif not resume_files or len(resume_files) == 0:
        st.error("Please upload at least one resume to analyze.")
    else:
        with st.spinner("Parsing Job Description and Resumes..."):
            if jd_file.type == "text/plain":
                jd_text = StringIO(jd_file.getvalue().decode("utf-8")).read()
            else:
                from pdfminer.high_level import extract_text
                temp_jd_path = save_uploaded_file(jd_file)
                jd_text = extract_text(temp_jd_path)

            ranker = CandidateRanker(jd_text)
            jd_skills_weights = ranker.jd_skill_weights
            st.write(f"**Extracted JD Skills with Weights:** {jd_skills_weights}")

            candidates = []
            progress_bar = st.progress(0)
            for i, file in enumerate(resume_files):
                temp_resume_path = save_uploaded_file(file)
                candidate = parse_resume(temp_resume_path, list(jd_skills_weights.keys()))
                candidates.append(candidate)
                progress = (i + 1) / len(resume_files)
                progress_bar.progress(progress)

            ranked_candidates = ranker.rank_candidates(candidates)

            # Search box to filter candidates by name or skill
            search_term = st.text_input("🔍 Search candidates by name or skill")

            filtered_candidates = []
            for c in ranked_candidates:
                if search_term.strip() == "":
                    filtered_candidates.append(c)
                else:
                    name = c.get("name", "").lower()
                    skills = " ".join(c.get("skills", [])).lower()
                    if search_term.lower() in name or search_term.lower() in skills:
                        filtered_candidates.append(c)

            # Prepare display data with expandable skill preview
            display_data = []
            for i, c in enumerate(filtered_candidates, 1):
                display_data.append({
                    "Rank": i,
                    "Name": c.get("name", ""),
                    "Email": c.get("email", ""),
                    "Score": f"{c.get('score', 0):.2f}",
                    "Matched Skills": ", ".join(c.get("skills", []))
                })

            df = pd.DataFrame(display_data)

        st.success("Analysis complete! See results below.")
        st.dataframe(df, use_container_width=True, height=600)

        # Clean up newlines and whitespace in all columns before exporting
        df = df.map(lambda x: str(x).replace("\n", " ").strip() if isinstance(x, str) else x)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📅 Download Ranking CSV",
            data=csv,
            file_name="ranking_output.csv",
            mime="text/csv"
        )
