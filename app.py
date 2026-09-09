import streamlit as st
import pandas as pd

if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

st.set_page_config(page_title="Agentic QE Requirement Advisor", layout="wide")

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            180deg,
            #F7FAFF 0%,
            #EEF4FF 100%
        );
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


if not st.session_state.show_analysis:

#    st.title("🤖 Agentic QE Requirement Advisor")

    st.markdown("""
<div style="
background: linear-gradient(135deg,#0B3D91,#0066CC);
padding:30px;
border-radius:16px;
color:white;
margin-bottom:20px;
">

<h1 style="margin:0;color:white;">
🤖 Agentic QE Requirement Advisor
</h1>

<p style="font-size:20px;color:white;">
Transform Ambiguous Requirements into Test-Ready Specifications
</p>

<p style="color:white;">
Requirements Quality | Testability | Acceptance Criteria | QE Scenarios
</p>

</div>
""", unsafe_allow_html=True)

    if st.button("🚀 Start Requirement Analysis"):
        st.session_state.show_analysis = True
        st.rerun()

    st.stop()

if st.button("⬅ Back to Home"):
    st.session_state.show_analysis = False
    st.rerun()

st.markdown(
    "<p style='color:#0B3D91;font-size:14px;font-weight:600;'>🏦 AI-Powered BFS Requirement Quality Engineering Assistant</p>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:8px;margin:0 0 8px 0;">
        <img src="https://img.icons8.com/fluency/32/bank-building.png" alt="BFS" style="width:22px;height:22px;" />
        <span style="color:#0B3D91;font-size:12px;font-weight:600;">
            Specialized for Banking &amp; Financial Services (BFS) Requirements
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
# ---------- Session State Defaults ----------
defaults = {
    "requirement_text": "",
    "requirement_id": " ",
    "auto_score": True,
    "clarity": 75,
    "completeness": 70,
    "testability": 72,
    "manual_quality_score": 72.3,
    "pci_dss": False,
    "auth_controls": False,
    "audit_trail": False,
    "fraud_prevention": False,
    "ai_advisory": None,
    "advisory_report_text": "",
    "clear_request": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def bounded(score: float) -> int:
    return max(0, min(100, int(round(score))))


def keyword_hits(text: str, keywords: list[str]) -> int:
    t = text.lower()
    return sum(1 for kw in keywords if kw in t)


def get_maturity_level(quality_score: float) -> str:
    if quality_score < 40:
        return "📄 Level 1 - Initial"
    if quality_score <= 59:
        return "📝 Level 2 - Draft"
    if quality_score <= 74:
        return "✅ Level 3 - Defined"
    if quality_score <= 89:
        return "🚀 Level 4 - Review Ready"
    return "🏆 Level 5 - QE Ready"


def analyze_requirement(text: str) -> dict:
    t = text.lower().strip()
    text_len = len(t)

    clarity_hits = keyword_hits(
        t,
        [
            "must",
            "shall",
            "required",
            "user",
            "customer",
            "system",
            "application",
            "service"
        ]
    )

    completeness_hits = keyword_hits(
        t,
        [
            "validate",
            "mandatory",
            "field",
            "input",
            "loan",
            "account",
            "customer",
            "transaction",
            "payment",
            "balance"
        ]
    )

    testability_hits = keyword_hits(
        t,
        [
            "test",
            "verify",
            "expected",
            "response",
            "error",
            "success",
            "reject",
            "approve",
            "validate",
            "mandatory",
            "input",
            "submission",
            "transaction",
            "account"
        ]
    )

    structure_hits = keyword_hits(t, ["if", "when", "then", "within"])
    measurable_hits = keyword_hits(t, ["%", "seconds", "ms", "days", "hours"])
    has_digits = any(ch.isdigit() for ch in t)

    clarity = 45 + (clarity_hits * 12) + (structure_hits * 4) + (5 if has_digits else 0)
    completeness = 40 + (completeness_hits * 12) + (structure_hits * 3)
    testability = 40 + (testability_hits * 12) + (measurable_hits * 6) + (5 if has_digits else 0)

    if text_len >= 120:
        clarity += 8
        completeness += 10
        testability += 8

    clarity = bounded(clarity)
    completeness = bounded(completeness)
    testability = bounded(testability)
    quality_score = round((clarity + completeness + testability) / 3, 1)

    if quality_score > 95:
        quality_score = 95

    maturity_level = get_maturity_level(quality_score)

    pci_dss = keyword_hits(t, ["pci", "pci dss", "cardholder"]) > 0
    auth_controls = keyword_hits(t, ["authentication", "auth", "login", "password", "mfa", "otp"]) > 0
    audit_trail = keyword_hits(t, ["audit", "audit trail", "log", "trace"]) > 0
    fraud_prevention = keyword_hits(t, ["fraud", "suspicious", "anomaly", "velocity"]) > 0

    if text_len < 50:
        risk_level = "High"
        readiness = "Low"
    else:
        risk_level = "Low" if quality_score >= 75 else "Medium" if quality_score >= 50 else "High"
        readiness = "High" if quality_score >= 85 else "Medium" if quality_score >= 70 else "Low"

    return {
        "clarity": clarity,
        "completeness": completeness,
        "testability": testability,
        "quality_score": quality_score,
        "maturity_level": maturity_level,
        "risk_level": risk_level,
        "readiness": readiness,
        "pci_dss": pci_dss,
        "auth_controls": auth_controls,
        "audit_trail": audit_trail,
        "fraud_prevention": fraud_prevention,
    }


def build_ai_advisory(text: str, analyzed: dict) -> dict:
    t = text.lower().strip()

    strengths = []
    identified_gaps = []
    compliance_notes = []
    recommended_next_actions = []

    if analyzed["clarity"] >= 75:
        strengths.append("Requirement uses clear directive language (e.g., must/shall/required).")
    if analyzed["completeness"] >= 75:
        strengths.append("Good coverage of inputs/validation details is indicated.")
    if analyzed["testability"] >= 75:
        strengths.append("Testability cues are present (test/verify/expected/measurable terms).")
    if len(t) >= 120:
        strengths.append("Requirement has adequate detail length for downstream analysis.")
    if not strengths:
        strengths.append("Baseline intent is present and can be strengthened with clearer acceptance details.")

    if len(t) < 50:
        identified_gaps.append("Requirement is too short; scope, rules, and outcomes are likely incomplete.")
    if analyzed["clarity"] < 70:
        identified_gaps.append("Ambiguous phrasing detected; add specific and measurable wording.")
    if analyzed["completeness"] < 70:
        identified_gaps.append("Missing completeness signals (mandatory fields, validation, business rules).")
    if analyzed["testability"] < 70:
        identified_gaps.append("Expected outcomes/test conditions are not explicit enough.")
    if "error" not in t and "exception" not in t:
        identified_gaps.append("Error/exception handling is not explicitly defined.")
    if not identified_gaps:
        identified_gaps.append("No major critical gaps detected at this rule-based level.")

    compliance_notes.append(f"PCI DSS: {'Detected' if analyzed['pci_dss'] else 'Not Detected'}")
    compliance_notes.append(
        f"Authentication Controls: {'Detected' if analyzed['auth_controls'] else 'Not Detected'}"
    )
    compliance_notes.append(f"Audit Trail: {'Detected' if analyzed['audit_trail'] else 'Not Detected'}")
    compliance_notes.append(
        f"Fraud Prevention: {'Detected' if analyzed['fraud_prevention'] else 'Not Detected'}"
    )

    recommended_next_actions.append("Add/confirm acceptance criteria with explicit expected outcomes.")
    recommended_next_actions.append("Add positive, negative, and boundary test conditions.")
    if not analyzed["pci_dss"]:
        recommended_next_actions.append("Clarify PCI DSS impact and cardholder-data handling requirements.")
    if not analyzed["auth_controls"]:
        recommended_next_actions.append("Define authentication/authorization controls (e.g., MFA, role checks).")
    if not analyzed["audit_trail"]:
        recommended_next_actions.append("Specify audit trail logging fields and retention expectations.")
    if not analyzed["fraud_prevention"]:
        recommended_next_actions.append("Include fraud-prevention checks (velocity/anomaly/risk rules).")
    if analyzed["risk_level"] == "High":
        recommended_next_actions.append("Run BA-QE clarification before development due to high requirement risk.")

    return {
        "strengths": strengths,
        "identified_gaps": identified_gaps,
        "compliance_notes": compliance_notes,
        "recommended_next_actions": recommended_next_actions,
    }


def _bullet_lines(items: list[str]) -> str:
    return "\n".join([f"- {item}" for item in items]) if items else "- None"


def generate_advisory_report(requirement_id: str, text: str, analyzed: dict, advisory: dict) -> str:
    t = text.lower().strip()

    confirmed_information = []
    if any(k in t for k in ["must", "shall", "required"]):
        confirmed_information.append("Directive/mandatory language is present.")
    if any(ch.isdigit() for ch in t):
        confirmed_information.append("Quantitative values are present in the requirement.")
    if "if" in t or "when" in t or "then" in t:
        confirmed_information.append("Conditional/flow structure keywords are present.")
    if not confirmed_information:
        confirmed_information.append("Baseline business intent is provided in requirement text.")

    assumptions = []
    if not any(k in t for k in ["user", "customer", "system", "application", "service"]):
        assumptions.append("Primary actor/system is assumed and should be explicitly stated.")
    if "within" not in t and "seconds" not in t and "ms" not in t and "hours" not in t and "days" not in t:
        assumptions.append("Performance/response-time expectations are assumed but not explicit.")
    if "error" not in t and "exception" not in t:
        assumptions.append("Error and exception behavior is assumed but not documented.")
    if not assumptions:
        assumptions.append("No major assumptions identified at this rule-based level.")

    clarification_needed = []
    if len(t) < 50:
        clarification_needed.append("Expand requirement scope and expected outcome details.")
    if analyzed["clarity"] < 70:
        clarification_needed.append("Clarify ambiguous statements using measurable language.")
    if analyzed["completeness"] < 70:
        clarification_needed.append("Clarify mandatory fields, business rules, and validation logic.")
    if analyzed["testability"] < 70:
        clarification_needed.append("Clarify expected outcomes and pass/fail criteria.")
    if not clarification_needed:
        clarification_needed.append("No critical clarification blockers detected.")

    missing_business_rules = []
    if "validate" not in t and "validation" not in t:
        missing_business_rules.append("Input validation/business validation rules are not explicit.")
    if "mandatory" not in t and "required" not in t:
        missing_business_rules.append("Mandatory vs optional field behavior is not explicit.")
    if "error" not in t and "exception" not in t:
        missing_business_rules.append("Error/exception handling rules are missing.")
    if "duplicate" not in t and "unique" not in t:
        missing_business_rules.append("Duplicate/uniqueness handling rules are missing.")
    if not missing_business_rules:
        missing_business_rules.append("No obvious missing business rules detected by current heuristics.")

    compliance_notes = advisory["compliance_notes"]

    acceptance_criteria = [
        "Given a valid input payload and required fields are provided, "
        "When the request is submitted, Then the system processes successfully and returns the expected result.",
        "Given invalid or missing mandatory input, "
        "When the request is submitted, Then the system rejects it with a clear validation message.",
        "Given a security/compliance-relevant transaction, "
        "When processing occurs, Then authentication checks and audit logging are enforced.",
    ]

    test_scenarios = {
        "Positive": [
            "Submit complete and valid data; verify successful processing.",
            "Verify expected outcome aligns with stated business intent.",
        ],
        "Negative": [
            "Submit missing mandatory fields; verify validation errors.",
            "Submit invalid format/type values; verify rejection and error messaging.",
        ],
        "Boundary": [
            "Test minimum allowed input values/lengths.",
            "Test maximum allowed input values/lengths.",
        ],
        "Security": [
            "Verify unauthorized access is blocked.",
            "Verify audit trail entry is generated for key actions.",
            "Verify compliance control flags for PCI/authentication/fraud where applicable.",
        ],
    }

    recommendations = advisory["recommended_next_actions"][:]
    recommendations.append("Validate final requirement with BA, QE, and compliance stakeholders.")
    recommendations.append("Baseline this report as pre-development quality evidence.")

    improvement_points = round(100 - float(analyzed["quality_score"]), 1)
    improvement_potential = (
        "Low" if analyzed["quality_score"] >= 85 else "Medium" if analyzed["quality_score"] >= 70 else "High"
    )

    report = f"""Agentic QE Requirement Advisor - Advisory Report
Requirement ID: {requirement_id}
Generated From: Rule-based analysis of user-entered requirement text

Requirement Text:
{text}

1. Executive Snapshot
- Quality Score: {analyzed['quality_score']}/100
- Readiness: {analyzed['readiness']}
- Risk Level: {analyzed['risk_level']}
- Improvement Potential: {improvement_points} pts ({improvement_potential})

2. Confirmed Information
{_bullet_lines(confirmed_information)}

3. Assumptions
{_bullet_lines(assumptions)}

4. Clarification Needed
{_bullet_lines(clarification_needed)}

5. Missing Business Rules
{_bullet_lines(missing_business_rules)}

6. Compliance Notes
{_bullet_lines(compliance_notes)}

7. Acceptance Criteria (Given / When / Then)
- AC1: {acceptance_criteria[0]}
- AC2: {acceptance_criteria[1]}
- AC3: {acceptance_criteria[2]}

8. Test Scenarios
- Positive
{_bullet_lines(test_scenarios['Positive'])}
- Negative
{_bullet_lines(test_scenarios['Negative'])}
- Boundary
{_bullet_lines(test_scenarios['Boundary'])}
- Security
{_bullet_lines(test_scenarios['Security'])}

9. Recommendations
{_bullet_lines(recommendations)}
"""
    return report


# ---------- Requirement Input ----------

if st.session_state.get("clear_request", False):
    st.session_state.requirement_text = ""
    st.session_state.clear_request = False

st.text_area(
    "Requirement Text",
    key="requirement_text",
    placeholder="Paste the requirement, user story, or BRD excerpt here before scoring...",
    height=180,
)

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button {
        background-color: #d32f2f !important;
        color: #ffffff !important;
        border: 1px solid #b71c1c !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button:hover {
        background-color: #b71c1c !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Analyze / Clear Buttons ----------
col_a, col_b = st.columns(2)

with col_a:
    analyze_clicked = st.button(
        "Analyze Requirement",
        type="primary",
        use_container_width=True
    )

with col_b:
    if st.button(
        "🗑 Clear Requirement",
        use_container_width=True
    ):
        st.session_state.ai_advisory = None
        st.session_state.advisory_report_text = ""

        st.session_state.clarity = 75
        st.session_state.completeness = 70
        st.session_state.testability = 72
        st.session_state.manual_quality_score = 72.3

        st.session_state.clear_request = True

        st.rerun()

# ---------- Analyze Logic ----------

if analyze_clicked:

    req_text = st.session_state.requirement_text.strip()

    if not req_text:
        st.warning("Please paste requirement text before analyzing.")

    else:

        analyzed = analyze_requirement(req_text)

        st.session_state.clarity = analyzed["clarity"]
        st.session_state.completeness = analyzed["completeness"]
        st.session_state.testability = analyzed["testability"]
        st.session_state.manual_quality_score = analyzed["quality_score"]
        
#       st.session_state.explainable_scoring = analyzed["explainable_scoring"]

        st.session_state.pci_dss = analyzed["pci_dss"]
        st.session_state.auth_controls = analyzed["auth_controls"]
        st.session_state.audit_trail = analyzed["audit_trail"]
        st.session_state.fraud_prevention = analyzed["fraud_prevention"]

        advisory = build_ai_advisory(req_text, analyzed)

        st.session_state.ai_advisory = advisory
        st.session_state.advisory_report_text = generate_advisory_report(
            st.session_state.requirement_id,
            req_text,
            analyzed,
            advisory,
        )

        st.success(
            "Analysis is completed. Scores, Snapshot and Advisory report are updated. Its ready to download."
        )

# ---------- Inputs ----------

if st.session_state.ai_advisory is not None:

    # UI removed; keep values for downstream logic compatibility
    requirement_id = st.session_state.get("requirement_id", "")
    auto_score = st.session_state.get("auto_score", True)

    c1, c2, c3 = st.columns(3)

    with c1:
        clarity = st.slider(
            "Clarity Score",
            0,
            100,
            key="clarity"
        )

    with c2:
        completeness = st.slider(
            "Completeness Score",
            0,
            100,
            key="completeness"
        )

    with c3:
        testability = st.slider(
            "Testability Score",
            0,
            100,
            key="testability"
        )
# ---------- Risk logic ----------
def risk_level(score: float) -> str:
    if score < 50:
        return "High"
    if score < 75:
        return "Medium"
    return "Low"


def readiness_level(score: float, text: str) -> str:
    if len(text.strip()) < 50:
        return "Low"
    if score >= 85:
        return "High"
    if score >= 70:
        return "Medium"
    return "Low"


def improvement_band(score: float) -> str:
    if score >= 85:
        return "Low"
    if score >= 70:
        return "Medium"
    return "High"


requirement_text = st.session_state.requirement_text

clarity = st.session_state.clarity
completeness = st.session_state.completeness
testability = st.session_state.testability
quality_score = st.session_state.manual_quality_score
ambiguity_risk = risk_level(clarity)
coverage_gap_risk = risk_level(completeness)
validation_risk = risk_level(testability)
overall_risk = risk_level(quality_score)
if len(requirement_text.strip()) < 50 and requirement_text.strip():
    overall_risk = "High"

readiness = readiness_level(quality_score, requirement_text)
improvement_points = round(100 - float(quality_score), 1)
improvement_potential = f"{improvement_points} pts ({improvement_band(quality_score)})"

analysis_completed = st.session_state.ai_advisory is not None

# ---------- Analysis Display Gate ----------
# Show analysis sections only after a successful analysis
analysis_completed = (
    st.session_state.get("ai_advisory") is not None
    and bool(st.session_state.get("requirement_text", "").strip())
)

if not analysis_completed:
    # Keep only requirement input + action buttons visible
    st.stop()


# ---------- Executive Snapshot ----------
quality_score = st.session_state.manual_quality_score

maturity_level = get_maturity_level(quality_score)
maturity_help = """Requirement Maturity Model

📄 Level 1 - Initial
Requirement is vague, ambiguous, and incomplete.

📝 Level 2 - Draft
Basic requirement exists but important details are missing.

✅ Level 3 - Defined
Requirement is reasonably clear and testable.

🚀 Level 4 - Review Ready
Requirement is complete, testable, and suitable for QE review.

🏆 Level 5 - QE Ready
Requirement is highly detailed, testable, compliant, and ready for implementation and testing.
"""

st.subheader("Executive Snapshot")
e1, e2, e3, e4 = st.columns(4)
e1.metric("Quality Score", f"{quality_score}/100")
e2.metric("Requirement Maturity Level", maturity_level, help=maturity_help)
e3.metric("Readiness", readiness)
e4.metric("Risk Level", overall_risk)

# ---------- AI Advisory Summary ----------
st.subheader("AI Advisory Summary")
advisory = st.session_state.get("ai_advisory")
if advisory:
    st.markdown("**1. Strengths**")
    for item in advisory["strengths"]:
        st.markdown(f"- {item}")

    st.markdown("**2. Identified Gaps**")
    for item in advisory["identified_gaps"]:
        st.markdown(f"- {item}")

    st.markdown("**3. Compliance Notes**")
    for item in advisory["compliance_notes"]:
        st.markdown(f"- {item}")

    st.markdown("**4. Recommended Next Actions**")
    for item in advisory["recommended_next_actions"]:
        st.markdown(f"- {item}")
else:
    st.markdown("Run **Analyze Requirement** to generate advisory insights.")

# ---------- BFS Compliance Assessment ----------

pci_dss = st.session_state.get("pci_dss", False)
auth_controls = st.session_state.get("auth_controls", False)
audit_trail = st.session_state.get("audit_trail", False)
fraud_prevention = st.session_state.get("fraud_prevention", False)

show_bfs_section = (
    pci_dss
    or auth_controls
    or audit_trail
    or fraud_prevention
)

if show_bfs_section:
    st.subheader("BFS Compliance Assessment")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        pci_dss = st.checkbox("PCI DSS", key="pci_dss")
    with b2:
        auth_controls = st.checkbox("Authentication Controls", key="auth_controls")
    with b3:
        audit_trail = st.checkbox("Audit Trail", key="audit_trail")
    with b4:
        fraud_prevention = st.checkbox("Fraud Prevention", key="fraud_prevention")

    controls = [pci_dss, auth_controls, audit_trail, fraud_prevention]
    coverage_pct = round((sum(controls) / len(controls)) * 100, 1)
    st.metric("Compliance Coverage", f"{coverage_pct}%")
    
# ---------- Dashboard ----------

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
st.table(risk_df)

# REMOVE this entire section:
# st.subheader("Dimension Comparison")
# chart_df = pd.DataFrame(
#     {
#         "Dimension": ["Clarity", "Completeness", "Testability", "Overall Quality"],
#         "Score": [clarity, completeness, testability, quality_score],
#     }
# ).set_index("Dimension")
# st.bar_chart(chart_df)

# ---------- Advisory Report ----------
st.subheader("Advisory Report")
report_text = st.session_state.get("advisory_report_text", "")
if report_text:
    st.text_area("Generated Advisory Report", value=report_text, height=520)
    safe_req_id = (requirement_id or "requirement").replace(" ", "_")
    st.download_button(
        label="Download Advisory Report",
        data=report_text,
        file_name=f"{safe_req_id}_advisory_report.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.info("Run **Analyze Requirement** to generate the advisory report.")

if requirement_text.strip():
#    st.caption(f"Requirement text captured ({len(requirement_text)} characters).")
     st.caption("✅ Report generated successfully")
else:
    st.caption("No requirement text provided yet.")

st.markdown(
    """
    <style>
    div[data-testid="stDownloadButton"] > button {
        background-color: #66BB6A !important;  /* light green */
        color: #FFFFFF !important;             /* white text */
        font-weight: 700 !important;           /* bold */
        border: 1px solid #4CAF50 !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #4CAF50 !important;  /* darker on hover */
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

prompt_text = (
    "AI Recommendation:\n"
    "• Add measurable response criteria\n"
    "• Define validation rules\n"
    "• Include negative scenarios\n"
    "• Specify error handling\n\n"
    "AI Recommendation:\n"
    "Requirement appears review-ready.\n"
    "Consider adding regulatory references and non-functional requirements "
    "to further strengthen QE readiness."
)
