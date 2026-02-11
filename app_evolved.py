import streamlit as st
from datetime import date
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Job Opportunity Portal",
    page_icon="💼",
    layout="wide"
)

# ---------------- Auto Refresh (every 60 seconds) ----------------
st_autorefresh(interval=60 * 1000, key="interview_refresh")

# ---------------- Colleges by State ----------------
colleges_by_state = {
    "Tamil Nadu": [
        "Anna University", "IIT Madras", "NIT Trichy", "VIT Vellore",
        "SRM IST", "PSG College of Technology", "SSN College of Engineering",
        "Thiagarajar College of Engineering", "SASTRA University",
        "Amrita Vishwa Vidyapeetham"
    ],
    "Karnataka": [
        "IISc Bangalore", "NIT Surathkal", "RV College of Engineering",
        "BMS College of Engineering", "MS Ramaiah Institute of Technology",
        "PES University", "Christ University", "Jain University"
    ],
    "Kerala": [
        "IIT Palakkad", "NIT Calicut", "CUSAT",
        "College of Engineering Trivandrum",
        "Government Engineering College Thrissur",
        "TKM College of Engineering", "MEC Kochi"
    ]
}

# ---------------- Jobs (All Degrees) ----------------
jobs = [

    # ---------- Engineering / IT ----------
    ["Infosys", "Software Trainee", ["BTech", "BE"], 60, 18, 28],
    ["TCS", "Assistant System Engineer", ["BTech", "BE"], 60, 18, 28],
    ["Wipro", "Project Engineer", ["BTech", "BE"], 60, 18, 27],
    ["Accenture", "Associate Software Engineer", ["BTech", "BE"], 65, 21, 28],
    ["ISRO", "Scientist/Engineer", ["BTech", "BE"], 65, 21, 28],

    # ---------- Data / Analytics ----------
    ["TCS", "Data Analyst Intern", ["BSc", "BTech"], 65, 21, 26],
    ["Infosys", "Data Science Trainee", ["BSc", "BTech"], 70, 21, 28],

    # ---------- BCA / MCA ----------
    ["Infosys", "Junior Developer", ["BCA", "MCA"], 60, 18, 28],
    ["Wipro", "System Support Engineer", ["BCA", "MCA"], 55, 18, 27],

    # ---------- BSc ----------
    ["Cognizant", "Operations Executive", ["BSc"], 55, 18, 25],
    ["Infosys", "BSc IT Trainee", ["BSc"], 60, 18, 26],

    # ---------- BCom ----------
    ["Deloitte", "Audit Executive", ["BCom"], 60, 21, 30],
    ["KPMG", "Accounts Associate", ["BCom"], 58, 21, 30],

    # ---------- BBA / MBA ----------
    ["HDFC Bank", "Relationship Officer", ["BBA", "MBA"], 55, 21, 30],
    ["ICICI Bank", "Management Trainee", ["MBA"], 60, 21, 30],

    # ---------- BA ----------
    ["Digital Marketing Firm", "Content Analyst", ["BA"], 55, 18, 28],
    ["Media House", "Junior Editor", ["BA"], 55, 21, 30],

    # ---------- Diploma ----------
    ["L&T", "Junior Technician", ["Diploma"], 55, 18, 30],
    ["TVS Motors", "Service Technician", ["Diploma"], 55, 18, 28],

    # ---------- Government / Any Degree ----------
    ["Banking Exam", "Clerk", ["Any"], 55, 20, 30],
    ["Banking Exam", "Probationary Officer", ["Any"], 60, 21, 30],
    ["SSC", "CGL Officer", ["Any"], 55, 18, 32],
    ["RRB", "NTPC Graduate", ["Any"], 55, 18, 33]
]

# ---------------- Session State ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- Page 1: Form ----------------
if st.session_state.page == "form":

    st.title("Job Opportunity Portal")
    st.subheader("Enter your details to find eligible jobs")

    today = date.today()
    max_dob = date(today.year - 18, today.month, today.day)

    with st.form("job_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            dob = st.date_input("Date of Birth *", max_value=max_dob)
            state = st.selectbox("State *", list(colleges_by_state.keys()))
            college = st.selectbox("College *", colleges_by_state[state])

        with col2:
            degree = st.selectbox(
                "Degree *",
                [
                    "Select",
                    "BTech", "BE", "BSc", "BCA",
                    "BCom", "BBA", "BA",
                    "MBA", "MCA",
                    "Diploma", "Any"
                ]
            )
            tenth = st.number_input("10th Percentage *", 0.0, 100.0)
            twelfth = st.number_input("12th Percentage *", 0.0, 100.0)
            photo = st.file_uploader("Upload Photo *", type=["jpg", "png"])
            certificate = st.file_uploader(
                "Upload Degree Certificate *",
                type=["jpg", "png", "pdf"]
            )

        submit = st.form_submit_button("Find Eligible Jobs")

    if submit:
        errors = []

        if not name.strip():
            errors.append("Full Name is required")
        if degree == "Select":
            errors.append("Please select a Degree")
        if tenth == 0 or twelfth == 0:
            errors.append("10th and 12th percentages are required")
        if photo is None:
            errors.append("Photo upload is required")
        if certificate is None:
            errors.append("Degree certificate upload is required")

        if errors:
            for e in errors:
                st.error(e)
        else:
            age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
            )
            avg_percent = (tenth + twelfth) / 2

            eligible = []
            for job in jobs:
                company, role, deg_list, min_per, min_age, max_age = job
                if (
                    (degree in deg_list or "Any" in deg_list)
                    and avg_percent >= min_per
                    and min_age <= age <= max_age
                ):
                    eligible.append([company, role, min_per, f"{min_age}-{max_age}"])

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ---------------- Page 2: Results ----------------
elif st.session_state.page == "result":

    st.title("Eligible Job Results")
    st.success(f"Hello {st.session_state.name}, Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        df = pd.DataFrame(
            st.session_state.eligible_jobs,
            columns=["Company", "Role", "Min % Required", "Age Limit"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No jobs found matching your eligibility")

    # ---------------- Live Interview Updates from CSV ----------------
    st.subheader("🔴 Live Interview Updates (Auto-Refreshing)")

    try:
        interviews = pd.read_csv("interviews.csv")
        st.dataframe(interviews, use_container_width=True)
        st.caption("Data auto-updates every 60 seconds from interviews.csv")
    except:
        st.error("Interview data file not found")

    if st.button("Go Back"):
        st.session_state.page = "form"
        st.rerun()
