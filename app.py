import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agentic QE Requirement Advisor", layout="wide")
st.title("🏦 Agentic QE Requirement Advisor")
st.caption("AI-Powered BFS Requirement Quality Engineering Assistant")

# ---------- Requirement Input ----------
requirement_text = st.text_area(
    "Requirement Text",
    placeholder="Paste the requirement, user story, or BRD excerpt here before scoring...",
    height=180,
)

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
    else st.number_input(
        "Quality Score",
        min_value=0.0,
        max_value=100.0,
        value=float(calculated_quality),
        step=0.1,
    )
)

# ---------- Risk logic ----------
def risk_level(score: float) -> str:
    if score < 50:
        return "High"
    if score < 75:
        return "Medium"
    return "Low"


def readiness_level(score: float) -> str:
    if score >= 85:
        return "Ready"
    if score >= 70:
        return "Partially Ready"
    return "Not Ready"


def improvement_band(score: float) -> str:
    if score >= 85:
        return "Low"
    if score >= 70:
        return "Medium"
    return "High"


ambiguity_risk = risk_level(clarity)
coverage_gap_risk = risk_level(completeness)
validation_risk = risk_level(testability)
overall_risk = risk_level(quality_score)

readiness = readiness_level(quality_score)
improvement_points = round(100 - float(quality_score), 1)
improvement_potential = f"{improvement_points} pts ({improvement_band(quality_score)})"

# ---------- Executive Snapshot ----------
st.subheader("Executive Snapshot")
e1, e2, e3, e4 = st.columns(4)
e1.metric("Quality Score", f"{quality_score}/100")
e2.metric("Readiness", readiness)
e3.metric("Risk Level", overall_risk)
e4.metric("Improvement Potential", improvement_potential)

# ---------- BFS Compliance Assessment ----------
st.subheader("BFS Compliance Assessment")
b1, b2, b3, b4 = st.columns(4)
with b1:
    pci_dss = st.checkbox("PCI DSS")
with b2:
    auth_controls = st.checkbox("Authentication Controls")
with b3:
    audit_trail = st.checkbox("Audit Trail")
with b4:
    fraud_prevention = st.checkbox("Fraud Prevention")

controls = [pci_dss, auth_controls, audit_trail, fraud_prevention]
coverage_pct = round((sum(controls) / len(controls)) * 100, 1)
st.metric("Compliance Coverage", f"{coverage_pct}%")

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

if requirement_text.strip():
    st.caption(f"Requirement text captured ({len(requirement_text)} characters).")
else:
    st.caption("No requirement text provided yet.")
