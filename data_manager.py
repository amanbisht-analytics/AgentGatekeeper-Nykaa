"""
Data Manager Module for Agent Gatekeeper – Nykaa
Handles storage and retrieval of registered AI agents (JSON) and audit logs (CSV).
No external database or API used.
"""

import os
import json
import csv
from datetime import datetime
import pandas as pd

# Paths configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
AGENTS_FILE = os.path.join(DATA_DIR, "agents.json")
AUDIT_LOG_FILE = os.path.join(DATA_DIR, "audit_log.csv")

AUDIT_LOG_COLUMNS = [
    "Date",
    "Time",
    "Customer",
    "Agent",
    "Action",
    "Amount",
    "Decision",
    "Rule",
    "Explanation"
]


def ensure_storage():
    """Ensure data directory and required storage files exist."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    if not os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(AUDIT_LOG_COLUMNS)


# -------------------------------------------------------------
# Agent Management Functions (JSON)
# -------------------------------------------------------------

def load_agents():
    """Load registered agents from the JSON file."""
    ensure_storage()
    try:
        with open(AGENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_agents(agents):
    """Save agents dictionary to the JSON file."""
    ensure_storage()
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(agents, f, indent=2)


def register_agent(agent_name):
    """
    Register an AI agent with current timestamp and 'Active' status.
    Returns: (success: bool, message: str)
    """
    clean_name = agent_name.strip()
    if not clean_name:
        return False, "Agent name cannot be empty."

    agents = load_agents()

    if clean_name in agents and agents[clean_name].get("status") == "Active":
        return False, f"Agent '{clean_name}' is already registered and Active."

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    agents[clean_name] = {
        "status": "Active",
        "registered_at": now_str,
        "revoked_at": None
    }
    save_agents(agents)
    return True, f"Agent '{clean_name}' successfully registered at {now_str}."


def revoke_agent(agent_name):
    """
    Revoke a registered AI agent, updating status and timestamping revocation.
    Returns: (success: bool, message: str)
    """
    clean_name = agent_name.strip()
    agents = load_agents()

    if clean_name not in agents:
        return False, f"Agent '{clean_name}' is not in the registry."

    if agents[clean_name].get("status") == "Revoked":
        revoked_time = agents[clean_name].get("revoked_at", "earlier")
        return False, f"Agent '{clean_name}' is already revoked (at {revoked_time})."

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    agents[clean_name]["status"] = "Revoked"
    agents[clean_name]["revoked_at"] = now_str
    save_agents(agents)
    return True, f"Agent '{clean_name}' has been revoked at {now_str}."


def get_agent_status(agent_name):
    """
    Get current status of an agent: 'Active', 'Revoked', or 'Unknown'.
    """
    clean_name = agent_name.strip()
    agents = load_agents()
    if clean_name not in agents:
        return "Unknown"
    return agents[clean_name].get("status", "Unknown")


# -------------------------------------------------------------
# Audit Log Functions (CSV)
# -------------------------------------------------------------

def append_audit_log(customer, agent, action, amount, decision, rule, explanation):
    """
    Append an evaluated request to the CSV audit log.
    Records date, time, customer, agent, action, amount, decision, rule, and explanation.
    """
    ensure_storage()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    row = [
        date_str,
        time_str,
        customer.strip(),
        agent.strip(),
        action.strip(),
        f"{float(amount):.2f}",
        decision.strip(),
        rule.strip(),
        explanation.strip()
    ]

    with open(AUDIT_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def load_audit_logs():
    """
    Load audit logs into a Pandas DataFrame.
    Returns DataFrame with AUDIT_LOG_COLUMNS.
    """
    ensure_storage()
    try:
        df = pd.read_csv(AUDIT_LOG_FILE)
        # Ensure all expected columns exist
        for col in AUDIT_LOG_COLUMNS:
            if col not in df.columns:
                df[col] = []
        return df
    except Exception:
        return pd.DataFrame(columns=AUDIT_LOG_COLUMNS)
