import streamlit as st
import os 

from parsers.pdf_parser import extractTextFromPDF
from parsers.docx_parser import extractTextFromDocx
from ai.jd_analyzer import analyzeJobDescription

from ai.resume_analyzer import analyze_resume
from ai.matcher import calculateMatchScore

from parsers.linkedin_parser import readLinkedinJSON

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = {}

st.set_page_config(
    page_title="HR Shortlisting Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 HR Resume Shortlisting Agent")

st.write("Upload a Job Description and candidate resumes.")

input_type = st.radio(
    "Choose Candidate Input Type",
    ["Resume", "Linkedin JSON"]
)

#Create data directories
os.makedirs("data/resumes", exist_ok=True)
os.makedirs("data/jds", exist_ok=True)

#Uploading Job Description
st.header("📌 Upload Job Description")
jd_file = st.file_uploader(
    "Upload Job Description",
    type=["txt"],
    key="jd_upload"
)

jd_text = ""

if jd_file is not None:
    try:
        jd_text = jd_file.read().decode("utf-8")
        
        st.success("Job Description uploaded successfully!")
        st.subheader("📄 Job Description Preview")

        st.text_area(
            "JD Content",
            jd_text,
            height=200
        )

        if st.button("Analyze Job Description"):
            with st.spinner("Analyzing JD with AI..."):
                st.session_state.jd_analysis = (analyzeJobDescription(jd_text=jd_text))

            st.subheader("🧠 AI JD Analysis")
            st.json(st.session_state.jd_analysis)
    
    except Exception as e:
        st.error(f"Error readin JD file: {e}")

#Uploading Resume
if input_type == "Resume":
    st.header("📌 Upload Resume")
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    all_resume_data = []

    if resume_file:
        for uploaded_file in resume_file:
            file_path = os.path.join("data/resumes", uploaded_file.name)

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            extracted_text = ""

            if uploaded_file.name.endswith(".pdf"):
                extracted_text = extractTextFromPDF(file_path)

            elif uploaded_file.name.endswith(".docx"):
                extracted_text = extractTextFromDocx(file_path)

            resume_analysis = analyze_resume(extracted_text)

            match_result = {}

            if st.session_state.jd_analysis:
                match_result = calculateMatchScore(st.session_state.jd_analysis, resume_analysis)

            all_resume_data.append({
                "filename": uploaded_file.name,
                "content": extracted_text,
                "analysis": resume_analysis,
                "match": match_result
            })

        st.success(f"{len(all_resume_data)} resumes uploaded successfully!")

    if all_resume_data:
        st.header("📑 Extracted Resume Text")

        all_resume_data = sorted (
            all_resume_data,
            key = lambda x:
                x["match"].get(
                    "match_score",
                    0
                ),
            reverse=True
        )

        st.header("🏆 Candidate Rankings")

        for index, resume in enumerate(all_resume_data, start=1):
            with st.expander(resume["filename"]):
                st.text_area(
                    "Resume Content",
                    resume["content"],
                    height=300
                )

                match_score = (resume["match"].get("match_score", 0))
                recommendation = (resume["match"].get("recommendation", "N/A"))
                candidate_name = (resume["analysis"].get("name", "Unknown"))

                if index == 1:
                    st.success("🏆 Top Candidate")
                st.markdown("---")

                st.markdown(
                    f"""
                ### #{index} - {candidate_name}

                🎯 Match Score: **{match_score}%**

                📌 Recommendation: **{recommendation}**
                """
                )

                st.progress(int(match_score))
                st.subheader("🧠 AI Resume Analysis")
                st.json(resume['analysis'])
                st.subheader("🎯 Match Analysis")
                st.json(resume["match"])

elif input_type == "Linkedin JSON":
    st.header("📌 Upload LinkedIn JSON")

    linkdin_file = st.file_uploader(
        "Upload Linkedin JSON", type=["json"],accept_multiple_files=True ,key="linkedin_upload"
    )

    if linkdin_file:
        all_linkedin_data = []
        for uploaded_file in linkdin_file:
            try:
                linkedin_data = readLinkedinJSON(uploaded_file)
                match_result = {}

                if st.session_state.jd_analysis:
                    match_result = calculateMatchScore(st.session_state.jd_analysis, linkedin_data)

                all_linkedin_data.append({
                    "filename": uploaded_file.name,
                    "profile": linkedin_data,
                    "match": match_result
                })

            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {e}")

        all_linkedin_data = sorted(
            all_linkedin_data,
            key = lambda x:
                x["match"].get(
                    "match_score",
                    0
                ), reverse= True
        )

        st.header("🏆 LinkedIn Candidate Rankings")

        for index, candidate in enumerate(all_linkedin_data, start=1):
            candidate_name = (candidate["profile"].get("name", "Unknown"))

            match_score = (candidate["match"].get("match_score"), 0)
            if isinstance(match_score, tuple):
                match_score = match_score[0]

            recommendation = (candidate["match"].get("recommendation", "N/A"))

            with st.expander(f"{index}. {candidate_name}"):
                if index == 1:
                    st.success("🏆 Top Candidate")
                    st.markdown(f"""
                    ### #{index} - {candidate_name}

                    🎯 Match Score: **{match_score}%**

                    📌 Recommendation: **{recommendation}**
                    """)

                    st.progress(int(match_score))
                    st.subheader("📄 LinkedIn Profile")
                    st.json(candidate["profile"])
                    st.subheader("🎯 Match Analysis")
                    st.json(candidate["match"])
