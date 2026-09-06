import streamlit as st
import pandas as pd

st.set_page_config(page_title="Requirement Quality Analyzer", layout="wide")
st.title("📊 Requirement Quality Analyzer")

# ---------- Inputs ----------
col1, col2 = st.columns([2, 1])

with col1:
    requirement_id = st.text_input("Requirement ID", value="REQ-001")
with col2:
    auto_score = st.toggle("Auto-calculate Quality Score", value=True)

c1, c2, c3 = st.columns(3)
with c1:
    clarity = st.slider("Clarity Score", 0, 100, 75)
with c2:
    completeness = st.slider("Completeness Score", 0, 100, 70)
with c3:
    testability = st.slider("Testability Score", 0, 100, 72)

calculated_quality = round((clarity + completeness + testability) / 3, 1)
quality_score = (
    calculated_quality
    if auto_score
    else st.number_input("Quality Score", min_value=0.0, max_value=100.0, value=float(calculated_quality), step=0.1)
)

# ---------- Risk logic ----------
def risk_level(score: float) -> str:
    if score < 50:
        return "High"
    if score < 75:
        return "Medium"
    return "Low"

ambiguity_risk = risk_level(clarity)
coverage_gap_risk = risk_level(completeness)
validation_risk = risk_level(testability)
overall_risk = risk_level(quality_score)

# ---------- Dashboard ----------
st.subheader("Scores")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Requirement ID", requirement_id if requirement_id else "N/A")
m2.metric("Quality Score", f"{quality_score}/100")
m3.metric("Clarity Score", f"{clarity}/100")
m4.metric("Completeness Score", f"{completeness}/100")
st.metric("Testability Score", f"{testability}/100")

st.progress(int(quality_score), text=f"Overall Quality: {quality_score}/100")

st.subheader("Quality Risk Indicators")
risk_df = pd.DataFrame(
    {
        "Indicator": [
            "Ambiguity Risk",
            "Coverage Gap Risk",
            "Validation Risk",
            "Overall Quality Risk",
        ],
        "Level": [ambiguity_risk, coverage_gap_risk, validation_risk, overall_risk],
    }
)
st.dataframe(risk_df, use_container_width=True, hide_index=True)

st.subheader("Dimension Comparison")
chart_df = pd.DataFrame(
    {
        "Dimension": ["Clarity", "Completeness", "Testability", "Overall Quality"],
        "Score": [clarity, completeness, testability, quality_score],
    }
).set_index("Dimension")
st.bar_chart(chart_df)