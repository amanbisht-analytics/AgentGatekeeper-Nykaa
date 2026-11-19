# Agent Gatekeeper – AI Agent Permission and Control System for Nykaa

- **Student Name:** Aman Bisht
- **Enrolment Number:** PGD202563127
- **Target Organization:** Nykaa (FSN E-Commerce Ventures Ltd.)
- **Project Type:** MBA College Assignment Prototype
- **Tool Used:** Google Antigravity (Gemini 3.8 Flash – High)

---

## 1. Project Overview & Context

This document maintains a complete engineering and evaluation audit trail of the prompts provided to **Google Antigravity** during the development of the **Agent Gatekeeper** prototype, along with the student's personal verification, testing, and validation records.

The application serves as a permission and governance gatekeeper regulating external AI shopping agents attempting to take actions on behalf of Nykaa customers across four core actions:
1. **View order**
2. **Place order**
3. **Return an order**
4. **Request a refund**

---

## 2. Main Prompts Given to Google Antigravity

### Prompt 1: Initial Prototype Generation & Architecture Setup
> **Objective:** Build a modular Streamlit web application implementing governance rules R1 through R7 for Nykaa's e-commerce ecosystem.
>
> **Requirements & Specifications:**
> - **Architecture & File Structure:**
>   - `app.py`: Main Streamlit web application with sidebar navigation across three sections: *Dashboard*, *Agent Management*, and *Request Evaluation & Audit Log*.
>   - `rules.py`: Separate, modular business rules engine strictly adhering to rule precedence:
>     - **R1:** Unknown or revoked agents $\rightarrow$ **`BLOCK`**
>     - **R2:** Registered active agent viewing an order $\rightarrow$ **`ALLOW`** (low-risk read-only action)
>     - **R3:** Registered active agent placing an order up to ₹2,000 $\rightarrow$ **`ALLOW`** (routine purchase within academic prototype threshold)
>     - **R4:** Registered active agent placing an order above ₹2,000 $\rightarrow$ **`ASK CUSTOMER`** (high-value confirmation)
>     - **R5:** Registered active agent requesting a return $\rightarrow$ **`ASK CUSTOMER`** (explaining verification of Nykaa's 15-day return window, intact packaging, and photo/video evidence)
>     - **R6:** Registered active agent requesting a refund $\rightarrow$ **`ASK CUSTOMER`** (monetary payout verification)
>     - **R7:** Zero or negative purchase/refund amounts $\rightarrow$ **`BLOCK`** (data integrity and fraud prevention)
>   - `data_manager.py`: Persistence layer handling JSON and CSV file operations without any database or external APIs.
>   - `data/agents.json`: AI agent registry capturing registration and revocation timestamps.
>   - `data/audit_log.csv`: Audit log recording Date, Time, Customer, Agent, Action, Amount, Decision, Rule, and Explanation.
>   - `requirements.txt`: Minimal dependencies (`streamlit`, `pandas`).
>   - `README.md`: Comprehensive documentation covering system rules, assignment context, and setup instructions.
> - **Student Identification:** Prominently display student name (`Aman Bisht`) and enrolment number (`PGD202563127`).
> - **Initial Data State:** Initialize with clean, empty data files for manual user evaluation.

---

### Prompt 2: Header Subtitle Contrast & Styling Fix
> **Objective:** Fix readability issues on the top banner subtitle container in `app.py`.
>
> **Issue Identified:** The original subtitle container used a light background (`#fff0f5`), causing the light text to have insufficient contrast.
>
> **Requested Fix:**
> - Update ONLY the CSS styling of `.student-badge` in `app.py`.
> - Apply Nykaa's signature deep pink background (`#FC2779`).
> - Apply crisp white text (`#FFFFFF`) to the text, bold tags, and code badges (`code { background-color: rgba(255, 255, 255, 0.25); color: #FFFFFF; }`).
> - Maintain high contrast and readability across both dark and light Streamlit themes without altering application logic or data files.

---

### Prompt 3: Custom / Unknown Agent Dynamic Input Fix
> **Objective:** Fix the Agent Source selector on the *Request Evaluation & Audit Log* page in `app.py`.
>
> **Issue Identified:** The radio selector between registered and custom agents was placed inside `st.form`. Because Streamlit forms do not rerun upon internal widget state changes, selecting *"Enter Custom / Unknown Agent"* failed to dynamically render a text input box.
>
> **Requested Fix:**
> - Move the `Agent Source` radio selector outside the `st.form` container so Streamlit triggers a reactive rerun upon selection.
> - When *"Enter Custom / Unknown Agent"* is chosen, dynamically display a clean `st.text_input` allowing the user to type any unregistered agent name (e.g., `UnknownBot`).
> - Retain the registered agents dropdown when *"Choose from Registered Agents"* is selected.
> - Ensure all R1–R7 rule evaluations, audit logging, styling, and data files remain completely intact.

---

## 3. Things I Personally Verified and Checked

During development and before final submission, the following steps were personally tested and verified:

1. **Environment & Runtime Verification:**
   - Verified Python 3.13.17 and Streamlit 1.67.0 installations in Windows PowerShell.
   - Confirmed proper working directory paths and package availability.

2. **Local Deployment & Browser Inspection:**
   - Launched the application locally from the terminal using:
     ```powershell
     py -m streamlit run app.py
     ```
   - Inspected the running UI in Google Chrome at `http://localhost:8501`.
   - Verified sidebar navigation across all three sections: *Dashboard*, *Agent Management*, and *Request Evaluation & Audit Log*.

3. **UI & Usability Issue Detection:**
   - **Visual Contrast:** Identified during live Chrome inspection that the subtitle banner had low contrast; requested and validated the deep pink (`#FC2779`) and crisp white (`#FFFFFF`) styling update.
   - **Form Reactivity:** Caught the Streamlit form isolation bug where the custom agent input did not appear dynamically; requested and confirmed the fix by placing the selector outside `st.form`.

4. **Agent Lifecycle & Audit Trail Validation:**
   - **Agent Registration:** Manually registered `"AmanShoppingAgent"`, confirming that its status was set to `Active` with an accurate registration date and timestamp in `data/agents.json`.
   - **Test Scenarios Execution:** Executed all mandatory test scenarios through the evaluation interface:
     - Unregistered / Revoked Agent $\rightarrow$ Rule **R1** (`BLOCK`)
     - Order View $\rightarrow$ Rule **R2** (`ALLOW`)
     - Order Placement $\le$ ₹2,000 (e.g., ₹1,500) $\rightarrow$ Rule **R3** (`ALLOW`)
     - Order Placement > ₹2,000 (e.g., ₹3,500) $\rightarrow$ Rule **R4** (`ASK CUSTOMER`)
     - Return Request $\rightarrow$ Rule **R5** (`ASK CUSTOMER`, displaying 15-day window, intact packaging, and evidence explanation)
     - Refund Request $\rightarrow$ Rule **R6** (`ASK CUSTOMER`)
     - Zero or Negative Amounts $\rightarrow$ Rule **R7** (`BLOCK`)
   - **Agent Revocation:** Revoked `"AmanShoppingAgent"` and verified that its status switched to `Revoked` with a recorded revocation date and timestamp.
   - **Audit Trail Persistence:** Verified that all evaluated requests appended rows to `data/audit_log.csv` with accurate timestamps and details.
   - **CSV Export:** Tested the *"Download Audit Log as CSV"* button and verified that the exported file was well-formed.
   - **Persistence Across Restarts:** Stopped and restarted the Streamlit server to confirm that registered agents and audit logs persisted without data loss.
