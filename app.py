import streamlit as st
import pandas as pd
import tempfile
import os
import time
from src.pipeline.prediction_pipeline import PredictionPipeline

# ================== BRAND CONFIG ==================
BRAND_NAME = "B-SpamGuard"
BRAND_TAGLINE = "My Blood • My Dream • My Legacy"
BRAND_DESC = "Cyber AI Email Threat Detection System"
AUTHOR = "Built by Bongu Rishi"
# ==================================================

# Page config
st.set_page_config(
    page_title=f"{BRAND_NAME} | Cyber Security AI",
    page_icon="B",
    layout="centered"
)

# ================== CYBER UI CSS ==================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0b0f19;
    color: #e6edf3;
}

h1, h2, h3 {
    color: #00f7ff;
    text-shadow: 0 0 10px #00f7ff;
}

.stButton>button {
    background: linear-gradient(90deg, #00f7ff, #0066ff);
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

.stButton>button:hover {
    box-shadow: 0 0 15px #00f7ff;
}

.stTextArea textarea {
    background-color: #020617;
    color: #e6edf3;
    border: 1px solid #00f7ff;
}

.stFileUploader {
    border: 1px dashed #00f7ff;
}

[data-testid="stMetricValue"] {
    color: #00ff88;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== PIPELINE ==================
@st.cache_resource
def get_pipeline():
    return PredictionPipeline(load_models=True)

pipeline = get_pipeline()

# ================== HEADER ==================
st.markdown(f"""
<div style="text-align:center">
    <h1> {BRAND_NAME}</h1>
    <h4>{BRAND_DESC}</h4>
    <p><i>{BRAND_TAGLINE}</i></p>
</div>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.markdown("##  SYSTEM PANEL")
st.sidebar.markdown("""
**Module:** B-SpamGuard  
**Status:**  Active  
**Engine:** NLP + ML  
**Security Level:** Enterprise  
""")

# ================== MAIN ==================
st.markdown("###  Email Threat Analysis Console")

tab1, tab2 = st.tabs([" Single Scan", " Bulk Scan"])

# ---- SINGLE ----
with tab1:
    email_text = st.text_area("Email Payload", height=200)

    if st.button(" SCAN EMAIL"):
        if email_text.strip():
            with st.spinner("Running threat analysis..."):
                result = pipeline.predict_single_email(email_text)
                prediction = result["prediction"]
                confidence = result.get("confidence", 0)

                if prediction == "Spam":
                    st.error(" THREAT IDENTIFIED — SPAM")
                else:
                    st.success(" CLEAN — NO THREAT")

                if confidence:
                    st.info(f"Confidence: {confidence:.1f}%")
        else:
            st.warning("Payload missing.")

# ---- BULK ----
with tab2:
    uploaded_file = st.file_uploader("Upload MBOX", type=["mbox", "txt"])

    if uploaded_file and st.button("⚡ START BULK SCAN"):
        with st.spinner("Scanning email database..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mbox") as tmp:
                tmp.write(uploaded_file.getvalue())
                path = tmp.name

            df = pipeline.predict_mbox_file(path)

            spam = len(df[df["Prediction"] == "Spam"])
            ham = len(df[df["Prediction"] == "Ham"])

            c1, c2, c3 = st.columns(3)
            c1.metric("Total", len(df))
            c2.metric("Threats", spam)
            c3.metric("Safe", ham)

            st.dataframe(df[["Time", "Subject", "Prediction"]].head(10))

            st.download_button(
                "⬇ DOWNLOAD REPORT",
                df.to_csv(index=False).encode("utf-8"),
                f"b_spamguard_cyber_report_{int(time.time())}.csv",
                "text/csv"
            )

            os.unlink(path)

# ================== FOOTER ==================
st.markdown("""
<hr>
<center>
<b>B-SpamGuard</b> © 2026<br>
Cyber Defense AI | Bongu Rishi<br>
<i>My Blood • My Legacy • My Brand</i>
</center>
""", unsafe_allow_html=True)
