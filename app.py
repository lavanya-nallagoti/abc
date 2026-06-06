import streamlit as st
import cv2
import pandas as pd
import numpy as np
import random
from fpdf import FPDF
import datetime

st.set_page_config(page_title="AI Healthcare System", layout="wide")

# ----------- SAFE UI STYLING -----------

st.markdown("""
<style>

/* App background */
.stApp{
background: linear-gradient(120deg,#f5f9ff,#eef7ff,#f3fff5);
}

/* Main title */
h1{
color:#0d47a1;
text-align:center;
font-weight:bold;
}

/* Section headings */
h2,h3{
color:#1a237e;
}

/* Sidebar background */
[data-testid="stSidebar"]{
background:#e3f2fd;
}

/* Labels */
label{
color:#000000 !important;
font-weight:600;
}

/* Checkbox text (Symptoms fix) */
.stCheckbox label{
color:#000000 !important;
font-size:16px;
}

/* Buttons */
div.stButton > button{
background:#1976d2;
color:white;
border-radius:8px;
padding:8px 20px;
font-size:16px;
}

div.stButton > button:hover{
background:#0d47a1;
}

/* Selectbox fix */
[data-baseweb="select"]{
color:black !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 AI Smart Healthcare System")

# ---------------- Sidebar Patient Details ----------------

st.sidebar.header("Patient Details")

name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age",1,100)
gender = st.sidebar.selectbox("Gender",["Male","Female"])
locality = st.sidebar.text_input("Locality")

time_now = datetime.datetime.now()

# ---------------- Symptoms Checker ----------------

st.header("Symptoms Checker")

symptoms_list = [
"Fever","Cough","Cold","Headache","Body Pain","Fatigue","Vomiting",
"Nausea","Chest Pain","Shortness of Breath","Dizziness","Sweating",
"Anxiety","Depression","Eye Pain","Eye Tiredness","Skin Rash",
"Allergy","Loss of Taste","Loss of Smell","Diarrhea","Constipation",
"Back Pain","Joint Pain","Muscle Pain","Weight Loss","Weight Gain",
"High Sugar","Low Sugar","High BP"
]

selected_symptoms = []

cols = st.columns(3)

for i,s in enumerate(symptoms_list):
    if cols[i%3].checkbox(s):
        selected_symptoms.append(s)

# ---------------- Vitals Monitoring ----------------

st.header("Vitals Monitoring")

bp = st.number_input("Blood Pressure")
temp = st.number_input("Body Temperature")
heart = st.number_input("Heart Rate")

# ---------------- Face Health Analysis ----------------

st.header("Face Health Analysis")

capture = st.button("Capture Face")

face_result = "Not Captured"

if capture:

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    ret,frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()

    if ret:

        st.image(frame,channels="BGR")

        conditions = [
        "Stress Detected",
        "Fatigue Detected",
        "Depression Risk",
        "Eye Tiredness",
        "Skin Allergy"
        ]

        face_result = random.choice(conditions)

        st.success("Face Health Result: "+face_result)

    else:
        st.error("Camera not detected")

# ---------------- Disease Prediction ----------------

st.header("Disease Prediction")

disease="Healthy"

if len(selected_symptoms)>5:
    disease="Flu"

if "Chest Pain" in selected_symptoms:
    disease="Heart Risk"

if "Skin Rash" in selected_symptoms:
    disease="Skin Allergy"

st.success("Predicted Condition: "+disease)

# ---------------- Medicine Recommendation ----------------

st.header("Medicine Recommendation")

med = {
"Flu":"Paracetamol + Rest",
"Heart Risk":"Consult Cardiologist",
"Skin Allergy":"Antihistamine",
"Healthy":"No medicine needed"
}

st.info(med.get(disease,"Consult Doctor"))

# ---------------- Patient History ----------------

st.header("Patient History Record")

if st.button("Save Record"):

    new_record = {
        "Name":name,
        "Age":age,
        "Gender":gender,
        "Locality":locality,
        "Time":str(time_now),
        "Symptoms":", ".join(selected_symptoms),
        "BP":bp,
        "Temp":temp,
        "Heart Rate":heart,
        "Face Result":face_result,
        "Disease":disease
    }

    try:
        history_df = pd.read_csv("patient_history.csv")
        history_df = pd.concat([history_df,pd.DataFrame([new_record])],ignore_index=True)

    except:
        history_df = pd.DataFrame([new_record])

    history_df.to_csv("patient_history.csv",index=False)

    st.success("Patient Record Saved!")

if st.button("Show Patient History"):

    try:
        st.dataframe(pd.read_csv("patient_history.csv"))

    except:
        st.warning("No patient data available.")

# ---------------- Medical Report Preview ----------------

st.header("Medical Report Preview")

report = {
"Name":name,
"Age":age,
"Gender":gender,
"Locality":locality,
"Time":str(time_now),
"Disease":disease,
"Symptoms":", ".join(selected_symptoms),
"BP":bp,
"Temperature":temp,
"Heart Rate":heart,
"Face Result":face_result,
"Suggested Medicine":med.get(disease,"Consult Doctor")
}

st.write(report)

# ---------------- Download PDF ----------------

if st.button("Download Medical Report"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial",size=12)

    pdf.cell(200,10,txt="AI Healthcare Medical Report",ln=True,align="C")

    pdf.ln(5)

    for k,v in report.items():
        pdf.cell(200,10,txt=f"{k} : {v}",ln=True)

    pdf_file="Medical_Report.pdf"

    pdf.output(pdf_file)

    with open(pdf_file,"rb") as f:
        st.download_button("Download PDF",f,file_name="Medical_Report.pdf")

# ---------------- Sidebar Chatbot ----------------

st.sidebar.markdown("---")
st.sidebar.header("💬 Medical Chatbot")

question = st.sidebar.text_input("Ask a health question")

if st.sidebar.button("Ask Chatbot"):

    answers = {
        "fever":"Drink water, rest, and take paracetamol if needed",
        "headache":"Take paracetamol and rest",
        "cold":"Use warm fluids and take rest",
        "cough":"Use cough syrup and stay hydrated",
        "fatigue":"Rest and multivitamins are recommended",
        "stress":"Meditation and relaxation exercises help"
    }

    found=False

    for key in answers:
        if key in question.lower():
            st.sidebar.success(answers[key])
            found=True
            break

    if not found:
        st.sidebar.info("Please consult a doctor.")