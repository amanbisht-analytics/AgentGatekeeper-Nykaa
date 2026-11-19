# Agent Gatekeeper – AI Agent Permission and Control System for Nykaa

**Student Name:** Aman Bisht  
**Enrolment Number:** PGD202563127  
**Target Organization:** Nykaa (FSN E-Commerce Ventures Ltd.)  
**Project Type:** MBA College Assignment Prototype  

---

## 1. Project Overview

With the rapid emergence of external AI shopping agents (e.g., shopping assistants, price comparison bots, personal AI delegates), e-commerce platforms like **Nykaa** require a robust governance and permission gatekeeper. 

**Agent Gatekeeper** is a lightweight, explainable decision-engine prototype that evaluates incoming requests from external AI agents before granting access to Nykaa's customer accounts.

The system enforces strict access control, ensures that high-value financial commitments and sensitive return/refund requests require explicit customer consent, and maintains a complete, tamper-evident audit trail for regulatory compliance.

---

## 2. Supported Actions

The gatekeeper evaluates four primary customer-delegated actions:
1. **View order**: Read-only access to customer order history.
2. **Place order**: Automated purchasing of beauty, wellness, and fashion items.
3. **Return an order**: Initiating a product return.
4. **Request a refund**: Requesting a direct monetary refund.

---

## 3. Governance Decision Rules

Requests are evaluated according to strict precedence:
1. **Agent Authentication Check** (Registration & Revocation status)
2. **Amount Validation** (Data integrity & fraud protection)
3. **Action-Specific Business Rules**

| Rule ID | Condition | Decision | Explanation |
| :--- | :--- | :---: | :--- |
| **R1** | Agent is unknown or revoked | **`BLOCK`** | External AI agents must be registered and active to interact with Nykaa accounts. |
| **R2** | Registered active agent viewing an order | **`ALLOW`** | Read-only action with low risk; safe to automate. |
| **R3** | Registered active agent placing an order $\le$ ₹2,000 | **`ALLOW`** | Routine low-value purchase below the auto-approval threshold. |
| **R4** | Registered active agent placing an order > ₹2,000 | **`ASK CUSTOMER`** | High-value order requiring direct customer OTP or explicit confirmation. |
| **R5** | Registered active agent requesting a return | **`ASK CUSTOMER`** | Customer must verify Nykaa's return conditions (15-day window, intact packaging, evidence). |
| **R6** | Registered active agent requesting a refund | **`ASK CUSTOMER`** | Direct monetary payout requires explicit customer consent and verification. |
| **R7** | Zero or negative purchase/refund amount | **`BLOCK`** | Invalid or corrupt transaction data blocked for security and fraud prevention. |

> **Note on Threshold:** The ₹2,000 threshold is an academic prototype limit established for this assignment and does not reflect official Nykaa corporate policy.

---

## 4. System Architecture & File Structure

The project is structured to keep business logic separate from storage and presentation:

```text
AgentGatekeeper-Nykaa/
│
├── app.py                 # Streamlit web application with sidebar navigation & Nykaa styling
├── rules.py               # Standalone decision rule engine (R1 through R7)
├── data_manager.py        # File-based persistence manager for JSON and CSV storage
│
├── data/
│   ├── agents.json        # AI agent registry (Active / Revoked with timestamps)
│   └── audit_log.csv      # Audit trail (Date, Time, Customer, Agent, Action, Amount, Decision, Rule, Explanation)
│
├── requirements.txt       # Dependencies (streamlit, pandas)
└── README.md              # Project documentation and student details
```

---

## 5. How to Run the Application

### Prerequisites
- Python 3.10+ (or Anaconda Python)
- Streamlit and Pandas

### Execution Command
Open a terminal in the project directory (`c:\Users\bisht\Desktop\AgentGatekeeper-Nykaa`) and run:

```bash
streamlit run app.py
```

Or using the full Anaconda Python path:

```powershell
& "C:\Users\bisht\anaconda3\python.exe" -m streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 6. Verification & Demonstration Guide

To demonstrate the full functionality for grading or academic review:

1. **Dashboard Section**:
   - Displays real-time metrics (Total Agents, Active, Revoked, Total Evaluated Requests, Decisions Breakdown).

2. **Agent Management Section**:
   - Register an agent (e.g., `Nykaa Beauty Assistant`). Verify it appears in the table with registration date and time.
   - Revoke an agent. Verify its status updates to `Revoked` with a recorded revocation date and time.

3. **Request Evaluation & Audit Log Section**:
   - **Test R1**: Submit a request with an unregistered agent name or a revoked agent $\rightarrow$ **`BLOCK`** (Rule R1).
   - **Test R2**: Select an active agent and action `View order` $\rightarrow$ **`ALLOW`** (Rule R2).
   - **Test R3**: Select an active agent, action `Place order`, and amount `₹1,200` $\rightarrow$ **`ALLOW`** (Rule R3).
   - **Test R4**: Select an active agent, action `Place order`, and amount `₹4,500` $\rightarrow$ **`ASK CUSTOMER`** (Rule R4).
   - **Test R5**: Select an active agent and action `Return an order` $\rightarrow$ **`ASK CUSTOMER`** (Rule R5, explaining the 15-day return window and packaging conditions).
   - **Test R6**: Select an active agent, action `Request a refund`, amount `₹1,500` $\rightarrow$ **`ASK CUSTOMER`** (Rule R6).
   - **Test R7**: Select an active agent, action `Place order`, and amount `0` or `-500` $\rightarrow$ **`BLOCK`** (Rule R7).
   - **Audit Trail**: Check that every evaluation automatically appends a new record to the audit table and CSV file.
   - **CSV Export**: Click "Download Audit Log as CSV" to export the audit trail.
