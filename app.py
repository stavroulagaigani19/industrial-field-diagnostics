import streamlit as st
from datetime import datetime
st.set_page_config(
    page_title="Field Diagnostics & Recovery Assistant",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Field Service Diagnostics & Work Instruction Tool")
st.caption("Standardized diagnostic, replacement, and recovery protocols for factory operators and field engineers.")
st.markdown("---")

procedures = {
    "ERR-301: Thermal Runaway / Overheating Pump": {
        "subsystem": "Cooling & Fluid Handling",
        "severity": "High (Machine Interlock)",
        "diagnostics": [
            "Check digital thermal sensor telemetry in SCADA dashboard (Normal: < 65°C).",
            "Perform non-contact IR thermometer scan on pump bearing housing.",
            "Verify coolant flow rate meter indicates at least 15 L/min.",
            "Inspect coolant supply lines for cavitation or manual valve throttling."
        ],
        "replacement": {
            "safety": ["Lockout / Tagout (LOTO) breaker #CB-04", "Wear heat-resistant gloves & eye protection"],
            "tools": ["13mm Socket wrench", "Torque wrench (rated to 25 Nm)", "Replacement Impeller/Pump Module (P/N: PM-8820)"],
            "steps": [
                "Isolate fluid line by turning manual valves V-101 and V-102 to fully closed.",
                "Disconnect electrical quick-release connector on motor housing.",
                "Unbolt 4x M8 retaining bolts using 13mm socket wrench.",
                "Remove damaged pump module and inspect seat gasket for debris.",
                "Install replacement module (P/N: PM-8820) and torque bolts cross-wise to 22 Nm."
            ]
        },
        "recovery": [
            "Re-open valves V-101 and V-102; check visually for leaks.",
            "Remove LOTO lock and restore breaker #CB-04.",
            "Run 5-minute dry-run idle test via engineering mode.",
            "Confirm temperature stabilizes below 55°C under nominal 80% load."
        ]
    },
    "ERR-104: Optical Alignment Sensor Drift": {
        "subsystem": "Vision & Metrology Station",
        "severity": "Medium (Degraded Accuracy)",
        "diagnostics": [
            "Inspect sensor lens for airborne dust, coolant mist, or scratch damage.",
            "Execute software calibration diagnostic script (Check delta offset).",
            "Verify 24V DC auxiliary power supply voltage stability using multimeter (Acceptable: 23.8V - 24.2V)."
        ],
        "replacement": {
            "safety": ["ESD wrist strap grounding mandatory", "Power down station via standard shutdown sequence"],
            "tools": ["Torx T10 precision driver", "Optical lens wipe (Lint-free)", "Sensor Unit (P/N: OPT-4410)"],
            "steps": [
                "Power down inspection station and connect ESD grounding strap.",
                "Carefully unplug the shielded M12 fieldbus connector.",
                "Loosen 2x T10 mounting screws on bracket.",
                "Mount new optical sensor (OPT-4410); hand-tighten screws initially to allow fine adjustment."
            ]
        },
        "recovery": [
            "Power on system and launch Metrology Calibration Tool.",
            "Place standard reference target gauge block (50.00 mm) in fixture.",
            "Execute 3 consecutive test cycles: standard deviation must be < 0.002 mm.",
            "Save calibration profile to station PLC memory."
        ]
    }
}

st.sidebar.header("Navigation & Filters")
selected_error = st.sidebar.selectbox("Select Incident / Error Code:", list(procedures.keys()))
data = procedures[selected_error]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Subsystem", value=data["subsystem"])
with col2:
    st.metric(label="Severity Level", value=data["severity"])
with col3:
    st.metric(label="Current Status", value="Ready for Action")

st.markdown("### Standard Operating Procedure (SOP)")

# Tabs για κάθε φάση (Diagnostics -> Replacement -> Recovery)
tab_diag, tab_repl, tab_recov, tab_signoff = st.tabs([
    "1. Diagnostics", 
    "2. Replacement Protocol", 
    "3. Recovery & Testing",
    "4. Sign-Off & Audit"
])

with tab_diag:
    st.subheader("🔍 Diagnostic Verification Steps")
    st.write("Perform the following non-invasive checks prior to physical intervention:")
    for idx, step in enumerate(data["diagnostics"], 1):
        st.checkbox(f"{idx}. {step}", key=f"diag_{idx}")

with tab_repl:
    st.subheader("⚙️ Component Replacement Procedure")
    
    c_safe, c_tool = st.columns(2)
    with c_safe:
        st.warning("⚠️ **Safety & PPE Requirements:**")
        for s in data["replacement"]["safety"]:
            st.markdown(f"- {s}")
    with c_tool:
        st.info("🔧 **Required Tools & Parts:**")
        for t in data["replacement"]["tools"]:
            st.markdown(f"- {t}")

    st.markdown("#### Sequential Replacement Actions")
    for idx, step in enumerate(data["replacement"]["steps"], 1):
        st.markdown(f"**Step {idx}:** {step}")

with tab_recov:
    st.subheader("✅ Recovery, Recalibration & Verification")
    st.write("Complete and verify all steps before releasing equipment back to production:")
    for idx, step in enumerate(data["recovery"], 1):
        st.checkbox(f"{idx}. {step}", key=f"recov_{idx}")

with tab_signoff:
    st.subheader("📝 Work Sign-Off & Continuous Improvement")
    operator_name = st.text_input("Operator / Field Engineer Name:")
    notes = st.text_area("Field Observations / Lessons Learned (Feedback for Design & IE team):", 
                         placeholder="e.g. Cable routing was tight; suggest lengthening harness by 50mm in next revision.")
    
    if st.button("Generate Completion Summary"):
        if operator_name:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"Work order signed off by **{operator_name}** at {timestamp}.")
            
            report = f"""
            ==================================================
            INDUSTRIAL ENGINEERING FIELD ACTION REPORT
            ==================================================
            Incident: {selected_error}
            Subsystem: {data['subsystem']}
            Completed by: {operator_name}
            Timestamp: {timestamp}
            
            Field Notes / Lessons Learned:
            {notes if notes else 'None reported.'}
            ==================================================
            """
            st.download_button(
                label="📥 Download Sign-Off Report (TXT)",
                data=report,
                file_name=f"Field_Action_Report_{selected_error[:7]}.txt",
                mime="text/plain"
            )
        else:
            st.error("Please enter your name to validate the sign-off.")
