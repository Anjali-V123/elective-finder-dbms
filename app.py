# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import python_connector as pc

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide", page_title="Elective Finder (Semester-aware)")

if 'role' not in st.session_state:
    st.session_state.role = None
if 'alumni_init_done' not in st.session_state:
    st.session_state.alumni_init_done = False
if 'student_init_done' not in st.session_state:
    st.session_state.student_init_done = False
if 'alumni_srn' not in st.session_state:
    st.session_state.alumni_srn = None
if 'alumni_projects' not in st.session_state:
    st.session_state.alumni_projects = []
if 'alumni_companies' not in st.session_state:
    st.session_state.alumni_companies = []
if 'student_interests' not in st.session_state:
    st.session_state.student_interests = []
if 'student_past_projects' not in st.session_state:
    st.session_state.student_past_projects = []
if 'student_companies_jobs' not in st.session_state:
    st.session_state.student_companies_jobs = []
if 'student_extra' not in st.session_state:
    st.session_state.student_extra = {}
if 'semester' not in st.session_state:
    st.session_state.semester = None

def reset_session():
    # Preserve app defaults but clear user inputs
    keys = list(st.session_state.keys())
    for k in keys:
        st.session_state.pop(k, None)
    st.session_state.role = None

def logout_button():
    if st.button("Logout"):
        reset_session()
        st.rerun()  # safe here because not inside callback

# -------------------------
# Home / Role selection
# -------------------------
if st.session_state.role is None:
    st.title("Elective Finder — Home")
    st.write("Select your role (no login required)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("I'm an Alumni"):
            st.session_state.role = 'alumni'
            st.rerun()
    with col2:
        if st.button("I'm a Student"):
            st.session_state.role = 'student'
            st.rerun()
    st.stop()

# Sidebar logout always visible
with st.sidebar:
    logout_button()

# -------------------------
# ALUMNI FLOW
# -------------------------
if st.session_state.role == 'alumni':
    st.header("Alumni — initial details")
    with st.form("alumni_form"):
        srn = st.text_input("SRN", value="")
        full_name = st.text_input("Full name", value="")
        dob = st.date_input("DOB (1995-2005)", min_value=date(1995,1,1), max_value=date(2005,12,31), value=date(2000,1,1))
        grad_year = st.slider("Graduated Year", 2015, 2024, 2022)
        # elective list from both semesters
        electives_all = pc.retrieve_electives(None)
        elective_list = sorted([e['Course_Name'] for e in electives_all])
        elective_choice = st.selectbox("Elective you studied (choose)", options=elective_list)
        submitted = st.form_submit_button("Submit alumni details")
    if submitted:
        if not srn or not full_name:
            st.error("Please fill SRN and full name")
        else:
            try:
                pc.insert_alumni_details(srn, full_name, dob.isoformat(), grad_year)
                st.session_state.alumni_init_done = True
                st.session_state.alumni_srn = srn
                st.success("Alumni details saved. Use sidebar to enter Feedback / Projects / Companies.")
                st.rerun()
            except Exception as e:
                st.error(f"DB error: {e}")

    if st.session_state.alumni_init_done:
        section = st.sidebar.radio("Alumni sections", ["Feedback", "Projects", "Companies", "View Data"])
        if section == "Feedback":
            st.subheader("Provide feedback for the elective")
            feedback = st.text_area("Feedback")
            grade = st.slider("Grade you received (0-100)", 0, 100, 80)
            if st.button("Submit feedback"):
                try:
                    pc.insert_alumni_elective_details(st.session_state.alumni_srn, elective_choice, feedback, grade)
                    st.success("Feedback recorded")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif section == "Projects":
            st.subheader("Add projects you worked on")
            proj_name = st.text_input("Project title")
            proj_year = st.number_input("Project year (YYYY)", min_value=2000, max_value=2100, value=2023)
            teachers = pc.all_teacher_names()
            mentor = st.selectbox("Mentor (Teacher)", options=teachers)
            if st.button("Add project"):
                try:
                    pc.insert_alumni_project_details(st.session_state.alumni_srn, proj_name, mentor, proj_year)
                    st.success("Project added")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif section == "Companies":
            st.subheader("Add companies and job roles")
            companies = pc.all_company_names()
            company = st.selectbox("Company", options=companies)
            jobs = pc.job_names_for_company(company)
            job_role = st.selectbox("Job role", options=jobs) if jobs else st.text_input("Job role")
            if st.button("Add company / job"):
                try:
                    pc.insert_alumni_job_details(st.session_state.alumni_srn, company, job_role)
                    st.success("Company/job recorded")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif section == "View Data":
            st.subheader("Demo data")
            st.write("Use a MySQL client to inspect the `electives` database tables or view sample rows below.")
            try:
                electives = pc.retrieve_electives(None)
                st.table(pd.DataFrame(electives))
            except Exception as e:
                st.error(f"Unable to fetch electives: {e}")

# -------------------------
# STUDENT FLOW
# -------------------------
elif st.session_state.role == 'student':
    st.header("Student — Choose semester")
    if st.session_state.semester is None:
        # choose semester
        sem = st.selectbox("Select semester", options=[5,6])
        if st.button("Continue"):
            st.session_state.semester = sem
            st.session_state.student_init_done = True
            st.rerun()
        st.stop()

    # student nav
    section = st.sidebar.radio("Student sections",
                               ["Select Interests","Select Past Projects","Select Dream Companies",
                                "Select Extra Details","Generate Your Perfect Elective"])
    st.subheader(f"Student - Semester {st.session_state.semester}")

    # Section: Interests
    if section == "Select Interests":
        st.subheader("Select up to 3 interests")
        interest_choices = ["Algorithms","NLP","Deep Learning","Data Analytics","Big Data","Computer Vision","Robotics","Cloud","IoT","Cyber Security","Blockchain"]
        selected = st.multiselect("Interests", interest_choices, default=st.session_state.student_interests, max_selections=3)
        if st.button("Save Interests"):
            st.session_state.student_interests = selected
            st.success("Interests saved")
        # show top 5 projects for chosen interest (one at a time)
        interest_for_search = st.selectbox("Choose an interest to see top projects", options=interest_choices)
        if st.button("See Top 5 Projects that match your interests"):
            rows = pc.retrieve_top_projects_by_interest(interest_for_search)
            if rows:
                st.table(pd.DataFrame(rows))
            else:
                st.info("No matching projects found. Try a different interest.")

    # Section: Past Projects
    elif section == "Select Past Projects":
        st.subheader("Add past project titles (press Add to append)")
        text = st.text_input("Project title")
        if st.button("Add past project"):
            if text:
                st.session_state.student_past_projects.append(text)
                st.success("Added")
        if st.session_state.student_past_projects:
            st.write("Your past projects:", st.session_state.student_past_projects)
        if st.button("See Top 5 Projects that match your past projects"):
            all_matches = []
            for p in st.session_state.student_past_projects:
                all_matches.extend(pc.retrieve_top_projects_by_pastproject(p))
            if all_matches:
                st.table(pd.DataFrame(all_matches))
            else:
                st.info("No matches")

    # Section: Dream Companies
    elif section == "Select Dream Companies":
        st.subheader("Choose company & job role pairs (press Add to append)")
        companies = pc.all_company_names()
        jobs_list = companies and pc.job_names_for_company(companies[0]) or []
        company = st.selectbox("Company", options=companies)
        job_options = pc.job_names_for_company(company)
        job = st.selectbox("Job Role", options=job_options) if job_options else st.text_input("Job role")
        if st.button("Add Company+Role"):
            st.session_state.student_companies_jobs.append((company, job))
            st.success("Added")
        if st.session_state.student_companies_jobs:
            st.write("Your choices:", st.session_state.student_companies_jobs)

    # Section: Extra Details
    elif section == "Select Extra Details":
        st.subheader("Pick extra preferences")
        difficulty = st.selectbox("Difficulty", ["", "EASY", "MEDIUM", "HARD", "EXTREME"])
        class_size = st.selectbox("Class size range", ["","0-50","50-100","100-150","150-200","200-250","250-300","300-350","350-400","400-450"])
        teachers = [""] + pc.all_teacher_names()
        teacher_choice = st.selectbox("Preferred Teacher", teachers)
        if st.button("Save Extra Details"):
            st.session_state.student_extra = {
                "difficulty": difficulty,
                "class_size": class_size,
                "teacher": teacher_choice
            }
            st.success("Saved")

    # Section: Generate
    elif section == "Generate Your Perfect Elective":
        st.subheader("Generate recommendation")
        # Count filled sections
        filled = 0
        if st.session_state.student_interests:
            filled += 1
        if st.session_state.student_past_projects:
            filled += 1
        if st.session_state.student_companies_jobs:
            filled += 1
        if st.session_state.student_extra:
            filled += 1
        if filled < 2:
            st.warning("Please fill in at least 2 navigation bar contents for an accurate result")
        else:
            semester = st.session_state.semester
            score_map = {}  # (cid,name) -> score

            # 1) Interests (weight 3.0)
            for interest in st.session_state.student_interests:
                try:
                    electives = pc.retrieve_top_electives_by_interest(interest, semester, limit=7)
                except Exception:
                    electives = []
                for e in electives:
                    cid = e['Course_ID']; name = e['Course_Name']; sc = e.get('score') or 0.0
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += float(sc) * 3.0

            # 2) Past projects (weight 2.0)
            for p in st.session_state.student_past_projects:
                try:
                    electives = pc.retrieve_top_electives_by_pastproject(p, semester, limit=7)
                except Exception:
                    electives = []
                for e in electives:
                    cid = e['Course_ID']; name = e['Course_Name']; sc = e.get('score') or 0.0
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += float(sc) * 2.0

            # 3) Companies & jobs (weight alumni_count * 1.0)
            for (comp, job) in st.session_state.student_companies_jobs:
                try:
                    ejs = pc.electives_based_on_jobs(comp, job, semester)
                except Exception:
                    ejs = []
                for e in ejs:
                    cid = e['Course_ID']; name = e['Course_Name']; cnt = e.get('alumni_count', 0)
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += float(cnt) * 1.0

            # 4) Teacher preference (flat +5)
            t = st.session_state.student_extra.get('teacher','')
            if t:
                try:
                    t_e = pc.electives_by_teacher(t, semester)
                except Exception:
                    t_e = []
                for e in t_e:
                    cid = e['Course_ID']; name = e['Course_Name']
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += 5.0

            # 5) Difficulty (flat +2)
            diff = st.session_state.student_extra.get('difficulty','')
            if diff:
                try:
                    d_e = pc.electives_by_difficulty(diff, semester)
                except Exception:
                    d_e = []
                for e in d_e:
                    cid = e['Course_ID']; name = e['Course_Name']
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += 2.0

            # 6) Class size (flat +1.5)
            cs = st.session_state.student_extra.get('class_size','')
            if cs:
                try:
                    low,high = [int(x) for x in cs.split('-')]
                    c_e = pc.electives_by_class_size_range(low, high, semester)
                except Exception:
                    c_e = []
                for e in c_e:
                    cid = e['Course_ID']; name = e['Course_Name']
                    score_map.setdefault((cid, name), 0.0)
                    score_map[(cid, name)] += 1.5

            # If score_map is empty, fallback to returning top electives by any fulltext match from interests or projects
            if not score_map:
                st.info("No electives scored from your inputs. Trying a fallback to top electives in this semester.")
                fallback = pc.retrieve_electives(semester)
                if fallback:
                    labels = [f"{r['Course_Name']} ({r['Course_ID']})" for r in fallback[:3]]
                    values = [1,1,1]
                    fig, ax = plt.subplots()
                    ax.pie(values, labels=labels, autopct='%1.1f%%')
                    st.pyplot(fig)
                    st.table(pd.DataFrame(fallback[:3]))
                else:
                    st.error("No electives available for this semester.")
            else:
                scored = sorted(score_map.items(), key=lambda kv: kv[1], reverse=True)
                top3 = scored[:3]
                labels = [f"{name} ({cid})" for ((cid,name),score) in top3]
                values = [score for ((cid,name),score) in top3]
                fig, ax = plt.subplots()
                ax.pie(values, labels=labels, autopct='%1.1f%%')
                ax.set_title("Top elective recommendations (pie chart)")
                st.pyplot(fig)
                df = pd.DataFrame([{"Course_ID":cid,"Course_Name":name,"Score":score} for ((cid,name),score) in top3])
                st.table(df)