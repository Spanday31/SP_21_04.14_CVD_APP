import streamlit as st
import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# ----- Page Configuration & Branding -----
st.set_page_config(layout="wide", page_title="SMART CVD Risk Reduction")

# Layout columns for logo
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=1000)
    else:
        st.warning("⚠️ Logo not found — please upload 'logo.png' into the app directory.")

# ----- Sidebar: Risk Profile -----
st.sidebar.markdown("### 🔹 Risk Profile")
age = st.sidebar.slider("Age", 30, 90, 60)
sex = st.sidebar.radio("Sex", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", 40.0, 200.0, 75.0)
height = st.sidebar.number_input("Height (cm)", 140.0, 210.0, 170.0)
bmi = weight / ((height / 100) ** 2)
st.sidebar.write(f"**BMI:** {bmi:.1f} kg/m²")
smoker = st.sidebar.checkbox("Current smoker")
diabetes = st.sidebar.checkbox("Diabetes")
egfr = st.sidebar.slider("eGFR (mL/min/1.73 m²)", 15, 120, 90)
st.sidebar.markdown("**Vascular Disease (tick all that apply)**")
vasc1 = st.sidebar.checkbox("Coronary artery disease")
vasc2 = st.sidebar.checkbox("Cerebrovascular disease")
vasc3 = st.sidebar.checkbox("Peripheral artery disease")
vasc_count = sum([vasc1, vasc2, vasc3])

# ----- Main Page: Panel 1 -----
st.title("SMART CVD Risk Reduction Calculator")

st.markdown("### Step 1: Lab Results")
total_chol = st.number_input("Total Cholesterol (mmol/L)", 2.0, 10.0, 5.2, 0.1)
hdl = st.number_input("HDL‑C (mmol/L)", 0.5, 3.0, 1.3, 0.1)
baseline_ldl = st.number_input("Baseline LDL‑C (mmol/L)", 0.5, 6.0, 3.0, 0.1)
crp = st.number_input("hs‑CRP (mg/L) — Baseline (not during acute MI)", 0.1, 20.0, 2.5, 0.1)
hba1c = st.number_input("Latest HbA₁c (%)", 4.5, 15.0, 7.0, 0.1)
tg = st.number_input("Fasting Triglycerides (mmol/L)", 0.5, 5.0, 1.5, 0.1)

st.markdown("---")

# ----- Panel 2: Therapies -----
st.markdown("### Step 2: Therapies")

st.subheader("Pre-admission Lipid‑lowering Therapy")
statin = st.selectbox("Statin (pre-admission)", ["None", "Atorvastatin 80 mg", "Rosuvastatin 20 mg"])
ez = st.checkbox("Ezetimibe 10 mg")
bemp = st.checkbox("Bempedoic acid")

# Anticipated LDL after current therapy
adj_ldl = baseline_ldl
if statin != "None":
    adj_ldl *= (1 - {"Atorvastatin 80 mg":0.50, "Rosuvastatin 20 mg":0.55}[statin])
if ez:
    adj_ldl *= (1 - 0.20)
adj_ldl = max(adj_ldl, 1.0)
st.write(f"**Anticipated LDL‑C:** {adj_ldl:.2f} mmol/L")

st.subheader("Add‑on Lipid‑lowering Therapy")
if adj_ldl > 1.8:
    pcsk9 = st.checkbox("PCSK9 inhibitor")
    incl = st.checkbox("Inclisiran (siRNA)")
else:
    st.info("PCSK9i/Inclisiran only if anticipated LDL‑C > 1.8 mmol/L")

st.markdown("**Lifestyle Changes**")
smoke_iv = st.checkbox("Smoking cessation", disabled=not smoker)
semaglutide = st.checkbox("GLP‑1 RA (Semaglutide)", disabled=(bmi < 30))
med_iv = st.checkbox("Mediterranean diet")
act_iv = st.checkbox("Physical activity")
alc_iv = st.checkbox("Alcohol moderation (>14 units/week)")
str_iv = st.checkbox("Stress reduction")

st.markdown("**Other Therapies**")
asa_iv = st.checkbox("Single antiplatelet (ASA or Clopidogrel)")
bp_iv = st.checkbox("BP control (target <130 mmHg)")
sglt2_iv = st.checkbox("SGLT2 i (e.g. Empagliflozin)")
if tg > 1.7:
    ico_iv = st.checkbox("Icosapent ethyl")
else:
    st.info("Icosapent ethyl only if TG > 1.7 mmol/L")

st.markdown("---")

# ----- Panel 3: Results & Summary -----
st.markdown("### Step 3: Results & Summary")

# (Insert SMART score calculation, ARR/RRR logic, and chart here)

st.markdown("---")
st.markdown("Created by Samuel Panday — 21/04/2025")
st.markdown("Created by PRIME team (Prevention Recurrent Ischaemic Myocardial Events)")
st.markdown("King’s College Hospital, London")
st.markdown("This tool is provided for informational purposes and designed to support discussions with your healthcare provider—it’s not a substitute for professional medical advice.")
