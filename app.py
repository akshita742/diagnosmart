import streamlit as st
import pandas as pd
import pickle
from disease_info import get_disease_info

# ----------------- LOAD DATA -----------------
symptom_data = pd.read_csv("data/symptom_disease.csv")

# ✅ Clean symptom names for UI
symptom_data['Symptom'] = symptom_data['Symptom'].str.replace('_', ' ').str.title()

all_symptoms = sorted(symptom_data['Symptom'].unique())

# ----------------- LOAD MODEL -----------------
with open("models/diagnosmart_model.pkl", "rb") as f:
    model = pickle.load(f)

# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="DiagnoSmart", layout="wide")
st.title("🩺 DiagnoSmart – AI Symptom Checker")

st.write("Select your symptoms below and get a possible diagnosis.")

# ✅ Searchable, multi-select symptom input
selected_symptoms = st.multiselect("Search or select symptoms:", options=all_symptoms)

# ----------------- PREDICT BUTTON -----------------
if st.button("🔍 Predict Disease"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        # ✅ Convert symptoms to model input format
        input_data = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
        prediction = model.predict([input_data])[0]

        st.success(f"### 🏥 Possible Disease: **{prediction}**")

        # ✅ Fetch extra info from Wikipedia or local DB
        st.write(get_disease_info(prediction))
