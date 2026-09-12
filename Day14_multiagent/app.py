import streamlit as st
import os

from agents.orchestrator import OrchestratorAgent


st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon="💼",
    layout="centered"
)


st.title("💼 AI Job Recommendation System")

st.write(
    "Upload your resume and find the jobs that best match your skills."
)


uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf", "txt"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button("🔍 Find Suitable Jobs"):

        # Get file extension
        file_extension = os.path.splitext(
            uploaded_file.name
        )[1]

        # Save uploaded resume temporarily
        temp_path = (
            f"data/uploaded_resume{file_extension}"
        )

        with open(temp_path, "wb") as file:

            file.write(
                uploaded_file.getbuffer()
            )


        with st.spinner(
            "Our AI agents are analyzing your resume..."
        ):

            orchestrator = OrchestratorAgent()

            result = orchestrator.run(
                temp_path
            )


        st.success(
            "Resume analysis completed!"
        )


        st.subheader(
            "🎯 Best Jobs for You"
        )

        st.markdown(
            result["ranked_jobs"]
        )