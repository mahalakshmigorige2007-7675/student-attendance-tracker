import streamlit as st
import json
import os
from datetime import date
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Attendance Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL CSS + BACKGROUND
# =========================================================

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background image */
.stApp {
    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.65),
            rgba(0, 0, 0, 0.65)
        ),
        url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=2000&q=80");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* Main heading */
.main-title {
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}


/* Subtitle */
.subtitle {
    text-align: center;
    color: #eeeeee;
    font-size: 17px;
    margin-bottom: 30px;
}


/* Cards */
.card {
    background: rgba(255, 255, 255, 0.96);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
    color: #111111;
}


/* Card headings */
.card h2,
.card h3,
.card h4 {
    color: #111111;
}


/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.96);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.20);
    color: #111111;
}

.metric-title {
    font-size: 15px;
    color: #555555;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111111;
}


/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(20, 20, 20, 0.96);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* Input labels */
label {
    color: #111111 !important;
    font-weight: 500 !important;
}


/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
}


/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}


/* Footer */
.footer {
    text-align: center;
    color: white;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FILE SETTINGS
# =========================================================

FILE_NAME = "attendance.json"


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except:
        return []


# =========================================================
# SAVE DATA
# =========================================================

def save_data(data):

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# =========================================================
# SESSION STATE
# =========================================================

if "attendance" not in st.session_state:
    st.session_state.attendance = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎓 Student Attendance Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart • Simple • Professional Attendance Management System</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Attendance System")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Attendance",
        "View Attendance",
        "Edit Attendance",
        "Delete Attendance",
        "Analytics"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Attendance Dashboard")

    data = st.session_state.attendance

    total_records = len(data)

    students = len(set(
        item["roll_no"] for item in data
    )) if data else 0

    present = sum(
        1 for item in data
        if item["status"] == "Present"
    )

    absent = sum(
        1 for item in data
        if item["status"] == "Absent"
    )

    percentage = (
        (present / total_records) * 100
        if total_records > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Records</div>
                <div class="metric-value">{total_records}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Students</div>
                <div class="metric-value">{students}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Present</div>
                <div class="metric-value">{present}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Attendance %</div>
                <div class="metric-value">{percentage:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ADD ATTENDANCE
# =========================================================

elif menu == "Add Attendance":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("➕ Add Student Attendance")

    with st.form("attendance_form"):

        col1, col2 = st.columns(2)

        with col1:
            roll_no = st.text_input(
                "Roll Number",
                placeholder="Example: 23A81A0501"
            )

            student_name = st.text_input(
                "Student Name",
                placeholder="Enter student name"
            )

        with col2:

            attendance_date = st.date_input(
                "Attendance Date",
                value=date.today()
            )

            status = st.selectbox(
                "Attendance Status",
                ["Present", "Absent"]
            )

        submitted = st.form_submit_button(
            "Save Attendance"
        )

        if submitted:

            if roll_no.strip() == "":
                st.error("Please enter Roll Number.")

            elif student_name.strip() == "":
                st.error("Please enter Student Name.")

            else:

                new_record = {
                    "roll_no": roll_no.strip(),
                    "student_name": student_name.strip(),
                    "date": str(attendance_date),
                    "status": status
                }

                st.session_state.attendance.append(new_record)

                save_data(st.session_state.attendance)

                st.success(
                    "Attendance record added successfully!"
                )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# VIEW ATTENDANCE
# =========================================================

elif menu == "View Attendance":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📋 Attendance Records")

    data = st.session_state.attendance

    if not data:

        st.info("No attendance records available.")

    else:

        df = pd.DataFrame(data)

        search = st.text_input(
            "🔍 Search by Roll Number or Student Name"
        )

        if search:

            df = df[
                df["roll_no"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                df["student_name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Attendance CSV",
            csv,
            "attendance.csv",
            "text/csv"
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EDIT ATTENDANCE
# =========================================================

elif menu == "Edit Attendance":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("✏️ Edit Attendance")

    data = st.session_state.attendance

    if not data:

        st.info("No records available to edit.")

    else:

        options = [
            f"{i} - {item['roll_no']} - {item['student_name']} - {item['date']}"
            for i, item in enumerate(data)
        ]

        selected = st.selectbox(
            "Select Record",
            options
        )

        index = int(selected.split(" - ")[0])

        record = data[index]

        new_roll = st.text_input(
            "Roll Number",
            value=record["roll_no"]
        )

        new_name = st.text_input(
            "Student Name",
            value=record["student_name"]
        )

        new_date = st.date_input(
            "Date",
            value=pd.to_datetime(
                record["date"]
            ).date()
        )

        new_status = st.selectbox(
            "Status",
            ["Present", "Absent"],
            index=0 if record["status"] == "Present" else 1
        )

        if st.button("💾 Update Record"):

            data[index] = {
                "roll_no": new_roll,
                "student_name": new_name,
                "date": str(new_date),
                "status": new_status
            }

            save_data(data)

            st.success(
                "Attendance updated successfully!"
            )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DELETE ATTENDANCE
# =========================================================

elif menu == "Delete Attendance":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🗑️ Delete Attendance")

    data = st.session_state.attendance

    if not data:

        st.info("No records available.")

    else:

        options = [
            f"{i} - {item['roll_no']} - {item['student_name']} - {item['date']}"
            for i, item in enumerate(data)
        ]

        selected = st.selectbox(
            "Select Record to Delete",
            options
        )

        index = int(selected.split(" - ")[0])

        if st.button("🗑️ Delete Record"):

            data.pop(index)

            save_data(data)

            st.success(
                "Attendance record deleted successfully!"
            )

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ANALYTICS
# =========================================================

elif menu == "Analytics":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📈 Attendance Analytics")

    data = st.session_state.attendance

    if not data:

        st.info("Add attendance records to view analytics.")

    else:

        df = pd.DataFrame(data)

        # -----------------------------------------
        # Student Attendance Percentage
        # -----------------------------------------

        summary = (
            df.groupby(
                ["roll_no", "student_name", "status"]
            )
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        if "Present" not in summary.columns:
            summary["Present"] = 0

        if "Absent" not in summary.columns:
            summary["Absent"] = 0

        summary["Total"] = (
            summary["Present"] +
            summary["Absent"]
        )

        summary["Attendance Percentage"] = (
            summary["Present"] /
            summary["Total"] * 100
        ).round(2)

        st.write("### 👨‍🎓 Student Attendance Percentage")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------------
        # Bar Chart
        # -----------------------------------------

        chart_data = summary[
            ["student_name", "Attendance Percentage"]
        ].set_index("student_name")

        st.write("### 📊 Attendance Percentage Chart")

        st.bar_chart(
            chart_data
        )

        # -----------------------------------------
        # Daily Attendance
        # -----------------------------------------

        daily = (
            df.groupby(
                ["date", "status"]
            )
            .size()
            .unstack(fill_value=0)
        )

        st.write("### 📅 Daily Attendance")

        st.line_chart(
            daily
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Student Attendance Tracker | Built with Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)