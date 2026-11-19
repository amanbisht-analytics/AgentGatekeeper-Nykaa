"""
Agent Gatekeeper – AI Agent Permission and Control System for Nykaa
Student: Aman Bisht | Enrolment Number: PGD202563127
MBA Assignment Project - Prototype for Nykaa

Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime

import data_manager
import rules

# -------------------------------------------------------------
# Page Configuration & Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Agent Gatekeeper | Nykaa",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal CSS for Nykaa theme and clear readability
st.markdown("""
<style>
    /* Main title accent */
    .nykaa-header {
        color: #fc2779;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .student-badge {
        background-color: #fc2779;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 10px 16px;
        font-size: 0.95rem;
        margin-bottom: 20px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(252, 39, 121, 0.2);
    }
    .student-badge strong {
        color: #ffffff;
    }
    .student-badge code {
        background-color: rgba(255, 255, 255, 0.25);
        color: #ffffff;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #fc2779;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .decision-allow {
        background-color: #d4edda;
        color: #155724;
        padding: 14px;
        border-radius: 6px;
        border-left: 5px solid #28a745;
        font-weight: 600;
        font-size: 1.15rem;
    }
    .decision-ask {
        background-color: #fff3cd;
        color: #856404;
        padding: 14px;
        border-radius: 6px;
        border-left: 5px solid #ffc107;
        font-weight: 600;
        font-size: 1.15rem;
    }
    .decision-block {
        background-color: #f8d7da;
        color: #721c24;
        padding: 14px;
        border-radius: 6px;
        border-left: 5px solid #dc3545;
        font-weight: 600;
        font-size: 1.15rem;
    }
</style>
""", unsafe_allow_html=True)

# Ensure storage files exist
data_manager.ensure_storage()

# -------------------------------------------------------------
# Sidebar: Student Details & Navigation
# -------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#fc2779;'>Nykaa Agent Gatekeeper</h2>", unsafe_allow_html=True)
st.sidebar.caption("AI Agent Permission & Control System")

# Student Details in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**Student Details**")
st.sidebar.text("Name: Aman Bisht")
st.sidebar.markdown("**Enrolment No:** `PGD202563127`")
st.sidebar.text("Company: Nykaa")
st.sidebar.text("Project: Academic Prototype")
st.sidebar.markdown("---")

# Navigation Menu
section = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Agent Management", "Request Evaluation & Audit Log"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Prototype Limit:\n"
    "Auto-approval threshold for placing orders is ₹2,000 (Academic prototype, not official Nykaa policy)."
)

# -------------------------------------------------------------
# Top Banner on Every Page
# -------------------------------------------------------------
st.markdown("<h1 class='nykaa-header'>Agent Gatekeeper – Nykaa</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='student-badge'>"
    "<strong>Student:</strong> Aman Bisht &nbsp;|&nbsp; "
    "<strong>Enrolment Number:</strong> <code>PGD202563127</code> &nbsp;|&nbsp; "
    "<strong>Target System:</strong> Nykaa AI Shopping Agent Governance"
    "</div>",
    unsafe_allow_html=True
)


# =============================================================
# SECTION 1: DASHBOARD
# =============================================================
if section == "Dashboard":
    st.subheader("System Overview Dashboard")
    st.write("Summary of registered external AI agents and evaluated customer action requests.")

    # Load current data
    agents = data_manager.load_agents()
    audit_df = data_manager.load_audit_logs()

    total_agents = len(agents)
    active_agents = sum(1 for a in agents.values() if a.get("status") == "Active")
    revoked_agents = sum(1 for a in agents.values() if a.get("status") == "Revoked")
    total_evaluations = len(audit_df)

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Agents", value=total_agents)
    with col2:
        st.metric(label="Active Agents", value=active_agents)
    with col3:
        st.metric(label="Revoked Agents", value=revoked_agents)
    with col4:
        st.metric(label="Evaluations Logged", value=total_evaluations)

    st.markdown("---")

    # Decision Breakdown
    st.subheader("Decision Breakdown")
    if total_evaluations > 0:
        decision_counts = audit_df["Decision"].value_counts().to_dict()
        allow_count = decision_counts.get("ALLOW", 0)
        ask_count = decision_counts.get("ASK CUSTOMER", 0)
        block_count = decision_counts.get("BLOCK", 0)

        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            st.metric(label="ALLOW", value=allow_count)
        with d_col2:
            st.metric(label="ASK CUSTOMER", value=ask_count)
        with d_col3:
            st.metric(label="BLOCK", value=block_count)
    else:
        st.info("No requests have been evaluated yet. Use 'Request Evaluation & Audit Log' to submit requests.")

    st.markdown("---")

    # Quick Rules Reference
    st.subheader("Configured Decision Rules (Summary)")
    rules_data = [
        {"Rule": "R1", "Condition": "Agent Unknown or Revoked", "Decision": "BLOCK", "Purpose": "Access control security"},
        {"Rule": "R2", "Condition": "Active agent viewing order", "Decision": "ALLOW", "Purpose": "Low-risk read-only action"},
        {"Rule": "R3", "Condition": "Active agent placing order <= ₹2,000", "Decision": "ALLOW", "Purpose": "Routine low-value purchase"},
        {"Rule": "R4", "Condition": "Active agent placing order > ₹2,000", "Decision": "ASK CUSTOMER", "Purpose": "Requires customer OTP/approval"},
        {"Rule": "R5", "Condition": "Active agent requesting return", "Decision": "ASK CUSTOMER", "Purpose": "Verify 15-day window & packaging"},
        {"Rule": "R6", "Condition": "Active agent requesting refund", "Decision": "ASK CUSTOMER", "Purpose": "Monetary payout verification"},
        {"Rule": "R7", "Condition": "Zero or negative purchase/refund amount", "Decision": "BLOCK", "Purpose": "Data integrity & fraud prevention"},
    ]
    st.table(pd.DataFrame(rules_data))


# =============================================================
# SECTION 2: AGENT MANAGEMENT
# =============================================================
elif section == "Agent Management":
    st.subheader("AI Agent Registration & Revocation")
    st.write("Manage authorized external shopping agents acting on behalf of Nykaa customers.")

    # Two columns: Register vs Revoke
    col_reg, col_rev = st.columns(2)

    with col_reg:
        st.markdown("### Register New AI Agent")
        with st.form("register_agent_form", clear_on_submit=True):
            new_agent_name = st.text_input(
                "Agent Name",
                placeholder="e.g., Nykaa Beauty Assistant, Google Shopping Agent"
            )
            submit_reg = st.form_submit_button("Register Agent", use_container_width=True)

            if submit_reg:
                if not new_agent_name.strip():
                    st.error("Please enter an agent name.")
                else:
                    success, msg = data_manager.register_agent(new_agent_name)
                    if success:
                        st.success(msg)
                    else:
                        st.warning(msg)

    with col_rev:
        st.markdown("### Revoke Registered AI Agent")
        agents = data_manager.load_agents()
        active_agent_names = [
            name for name, details in agents.items() if details.get("status") == "Active"
        ]

        if active_agent_names:
            with st.form("revoke_agent_form"):
                selected_agent_to_revoke = st.selectbox(
                    "Select Active Agent to Revoke",
                    active_agent_names
                )
                submit_rev = st.form_submit_button("Revoke Access", use_container_width=True)

                if submit_rev:
                    success, msg = data_manager.revoke_agent(selected_agent_to_revoke)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("No active agents available to revoke. Register an agent first.")

    st.markdown("---")

    # Registered Agents Table
    st.subheader("Registered Agents Registry")
    agents = data_manager.load_agents()
    if agents:
        agent_records = []
        for name, details in agents.items():
            agent_records.append({
                "Agent Name": name,
                "Status": details.get("status", "Unknown"),
                "Registered At": details.get("registered_at", "-"),
                "Revoked At": details.get("revoked_at") if details.get("revoked_at") else "-"
            })
        agents_df = pd.DataFrame(agent_records)
        st.dataframe(agents_df, use_container_width=True, hide_index=True)
    else:
        st.info("No agents registered yet. Use the registration form above.")


# =============================================================
# SECTION 3: REQUEST EVALUATION & AUDIT LOG
# =============================================================
elif section == "Request Evaluation & Audit Log":
    st.subheader("Request Evaluation")
    st.write("Submit an action request for an AI agent to evaluate against governance rules.")

    agents = data_manager.load_agents()
    registered_names = list(agents.keys())

    # Agent selection mode placed outside st.form so UI reruns dynamically on selection
    agent_input_mode = st.radio(
        "Agent Source",
        ["Choose from Registered Agents", "Enter Custom / Unknown Agent"],
        horizontal=True
    )

    # Evaluation Input Form
    with st.form("evaluation_form"):
        col_c, col_a = st.columns(2)
        with col_c:
            customer_name = st.text_input("Customer Name", value="Aman Bisht")

            if agent_input_mode == "Choose from Registered Agents":
                if registered_names:
                    agent_name = st.selectbox("Select Agent", registered_names)
                else:
                    st.info("No registered agents found. Register an agent in 'Agent Management' or switch to 'Enter Custom / Unknown Agent'.")
                    agent_name = ""
            else:
                agent_name = st.text_input(
                    "Agent Name",
                    placeholder="e.g., UnknownBot, PriceScraper-99",
                    help="Type any unregistered or custom agent name to test Rule R1 (BLOCK)."
                )

        with col_a:
            action = st.selectbox(
                "Requested Action",
                ["View order", "Place order", "Return an order", "Request a refund"]
            )
            amount = st.number_input(
                "Amount (₹)",
                value=1500.00,
                step=100.0,
                format="%.2f",
                help="Enter amount for purchase or refund. Enter 0 for read-only actions like viewing an order."
            )

        submit_eval = st.form_submit_button("Evaluate Request", use_container_width=True)

    # Processing Evaluation
    if submit_eval:
        if not customer_name.strip():
            st.error("Customer name cannot be empty.")
        elif not agent_name or not agent_name.strip():
            st.error("Agent name cannot be empty.")
        else:
            # 1. Determine agent status
            agent_status = data_manager.get_agent_status(agent_name)

            # 2. Evaluate request according to rules
            decision, rule_id, explanation = rules.evaluate_permission(
                customer=customer_name,
                agent=agent_name,
                action=action,
                amount=amount,
                agent_status=agent_status
            )

            # 3. Append to CSV Audit Log
            data_manager.append_audit_log(
                customer=customer_name,
                agent=agent_name,
                action=action,
                amount=amount,
                decision=decision,
                rule=rule_id,
                explanation=explanation
            )

            # 4. Display Decision to User
            st.markdown("### Evaluation Result")
            res_col1, res_col2 = st.columns([1, 2])

            with res_col1:
                if decision == "ALLOW":
                    st.markdown("<div class='decision-allow'>🟢 DECISION: ALLOW</div>", unsafe_allow_html=True)
                elif decision == "ASK CUSTOMER":
                    st.markdown("<div class='decision-ask'>🟠 DECISION: ASK CUSTOMER</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='decision-block'>🔴 DECISION: BLOCK</div>", unsafe_allow_html=True)

                st.write(f"**Applicable Rule:** `{rule_id}`")
                st.write(f"**Agent Status:** `{agent_status}`")

            with res_col2:
                st.markdown("**Explanation:**")
                st.info(explanation)

            st.success("Record saved to audit log successfully.")

    st.markdown("---")

    # Audit Log Display
    st.subheader("Audit Log Trail")
    st.write("Persistent record of all evaluated requests.")

    audit_df = data_manager.load_audit_logs()

    if not audit_df.empty:
        # Display with newest entries at the top
        st.dataframe(audit_df.iloc[::-1], use_container_width=True, hide_index=True)

        # Download CSV button
        csv_data = audit_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Audit Log as CSV",
            data=csv_data,
            file_name=f"nykaa_agent_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("The audit log is currently empty. Run an evaluation above to record the first transaction.")
