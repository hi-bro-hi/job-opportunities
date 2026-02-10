import streamlit as st
from datetime import date
import pandas as pd

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Job Opportunity Portal",
    page_icon="💼",
    layout="wide"
)

# ---------------- Sample Data ----------------
colleges_by_state = {
    "Tamil Nadu": ["Anna University", "SRM", "VIT", "PSG Tech"],
    "Karnataka": ["RV College", "BMS College", "IISc"],
    "Kerala": ["CUSAT", "NIT Calicut"]
}

jobs = [
    ["Infosys", "Software Trainee", ["BTech", "BE"], 60, 18, 28],
    ["TCS", "Data Analyst Intern", ["BSc", "BTech"], 65, 21, 26],
    ["Banking Exam", "Clerk", ["Any"], 55, 20, 30]
]

# ---------------- Session State for Two Pages ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- Page 1: Form ----------------
if st.session_state.page == "form":

    st.title("Job Opportunity Portal")
    st.subheader("Enter your details to find eligible jobs")

    with st.form("job_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            dob = st.date_input("Date of Birth")
            state = st.selectbox("State", list(colleges_by_state.keys()))
            college = st.selectbox("College", colleges_by_state[state])

        with col2:
            degree = st.selectbox("Degree", ["BTech", "BE", "BSc", "Any"])
            tenth = st.number_input("10th Percentage", 0.0, 100.0)
            twelfth = st.number_input("12th Percentage", 0.0, 100.0)
            photo = st.file_uploader("Upload Photo", type=["jpg", "png"])
            certificate = st.file_uploader("Upload Degree Certificate", type=["jpg", "png", "pdf"])

        submit = st.form_submit_button("Find Eligible Jobs")

    if submit:
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        avg_percent = (tenth + twelfth) / 2

        # Save data in session
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.degree = degree
        st.session_state.avg_percent = avg_percent

        # Job matching
        eligible = []
        for job in jobs:
            company, role, deg_list, min_per, min_age, max_age = job
            if (
                (degree in deg_list or "Any" in deg_list) and
                avg_percent >= min_per and
                min_age <= age <= max_age
            ):
                eligible.append([company, role, min_per, f"{min_age}-{max_age}"])
        st.session_state.eligible_jobs = eligible

        st.session_state.page = "result"
        st.rerun()

# ---------------- Page 2: Results ----------------
elif st.session_state.page == "result":

    st.title("Eligible Job Results")
    st.success(f"Hello {st.session_state.name}, your age is {st.session_state.age}")

    st.subheader("Eligible Job Opportunities")

    if st.session_state.eligible_jobs:
        df = pd.DataFrame(
            st.session_state.eligible_jobs,
            columns=["Company", "Role", "Min % Required", "Age Limit"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No jobs found for your eligibility")

    st.subheader("Live Interview Updates")
    # This simulates live updates; online deployment can later fetch real APIs
    st.info("""
    • Infosys – Chennai – 15 Feb 2026  
    • TCS – Bangalore – 18 Feb 2026  
    • Wipro – Hyderabad – 20 Feb 2026
    """)

    if st.button("Go Back"):
        st.session_state.page = "form"
        st.rerun()
