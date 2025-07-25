# app.py

import streamlit as st
from predictor import predict_disease_with_confidence, SYMPTOMS
from database import create_table, insert_prediction
from disease_info import get_disease_info
from first_aid import get_first_aid_info
from datetime import datetime
import re

# ✅ Initialize DB
create_table()

# ✅ PAGE CONFIG (adds logo & favicon)
st.set_page_config(
    page_title="DiagnoSmart",
    page_icon="🧠",   # can change to your logo later
    layout="wide"
)

# ✅ HEADER WITH LOGO & TAGLINE
st.markdown(
    """
    <div style="text-align:center">
        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966489.png" width="100">
        <h1 style="color:#2C3E50;">🧠 DiagnoSmart</h1>
        <p style="font-size:18px;">Your AI-powered Symptom-to-Disease Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔍 Search bar for symptoms
search_query = st.text_input("🔍 Search for a symptom:")

# ✅ Filter symptoms
if search_query:
    filtered_symptoms = [sym for sym in SYMPTOMS if search_query.lower() in sym.lower()]
    if not filtered_symptoms:
        st.warning("⚠️ No symptoms found for your search.")
else:
    filtered_symptoms = SYMPTOMS

# ✅ State management for checkboxes
if "checked_symptoms" not in st.session_state:
    st.session_state.checked_symptoms = {sym: False for sym in SYMPTOMS}

# ✅ Buttons: Select All / Clear All
colA, colB = st.columns([1, 1])
with colA:
    if st.button("✅ Select All (Filtered)"):
        for sym in filtered_symptoms:
            st.session_state.checked_symptoms[sym] = True
with colB:
    if st.button("❌ Clear All"):
        for sym in SYMPTOMS:
            st.session_state.checked_symptoms[sym] = False

# ✅ Multi-column symptom checkboxes
user_symptoms = {}
st.subheader("🩺 Check the symptoms you are experiencing:")

cols = st.columns(3)
for index, symptom in enumerate(filtered_symptoms):
    col = cols[index % 3]

    if search_query:
        pattern = re.compile(re.escape(search_query), re.IGNORECASE)
        highlighted_text = pattern.sub(lambda m: f"**{m.group(0)}**", symptom.replace("_", " ").capitalize())
    else:
        highlighted_text = symptom.replace("_", " ").capitalize()

    with col:
        user_symptoms[symptom] = st.checkbox(highlighted_text, value=st.session_state.checked_symptoms[symptom])
        st.session_state.checked_symptoms[symptom] = user_symptoms[symptom]

# ✅ Predict Button
if st.button("🔍 Predict Disease"):
    top_diseases = predict_disease_with_confidence(user_symptoms, top_k=3)

    st.subheader("📊 Prediction Results")
    for disease, confidence in top_diseases:
        st.success(f"✅ **{disease}** — {confidence}% confidence")

        with st.expander(f"ℹ️ Learn more about {disease}"):
            info = get_disease_info(disease)
            st.write(info)

            first_aid, urgency = get_first_aid_info(disease)
            if first_aid:
                st.markdown(f"**🆘 First Aid Tips:** {first_aid}")
                st.markdown(f"**⏱ Urgency:** {urgency}")
            else:
                st.warning("⚠️ No first aid info available for this disease yet.")

    insert_prediction(user_symptoms, top_diseases[0][0])
    st.caption(f"🕒 Prediction logged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ✅ FOOTER
st.markdown("---")
st.markdown("<p style='text-align:center;'>Built with  using Python + Streamlit • © 2025 DiagnoSmart</p>", unsafe_allow_html=True)
