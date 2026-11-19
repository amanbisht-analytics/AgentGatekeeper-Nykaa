"""
Decision Rules Module for Agent Gatekeeper – Nykaa
Student: Aman Bisht | Enrolment No: PGD202563127 | Nykaa MBA Prototype

Separated business rules logic to decide whether an external AI shopping agent
should be permitted to perform an action on behalf of a customer.

Available Actions:
1. View order
2. Place order
3. Return an order
4. Request a refund

Decisions:
- ALLOW: Action permitted automatically
- ASK CUSTOMER: Action requires direct customer consent or verification
- BLOCK: Action rejected for security, policy, or invalid data
"""

# Academic prototype limit for automated order placement (not official Nykaa policy)
ORDER_AUTO_APPROVAL_THRESHOLD = 2000.0


def evaluate_permission(customer, agent, action, amount, agent_status):
    """
    Evaluates an action request based on strict rule precedence:
    1. Agent registration & revocation check (R1)
    2. Amount validation for purchase / refund (R7)
    3. Action-specific rules (R2, R3, R4, R5, R6)

    Parameters:
        customer (str): Name of the Nykaa customer
        agent (str): Name of the AI agent requesting access
        action (str): One of the 4 supported actions
        amount (float): Monetary value associated with the action
        agent_status (str): Current status ('Active', 'Revoked', or 'Unknown')

    Returns:
        tuple: (decision, rule_number, explanation)
    """
    # -------------------------------------------------------------
    # Step 1: Agent Registration & Revocation Check
    # -------------------------------------------------------------
    if agent_status != "Active":
        if agent_status == "Revoked":
            status_desc = "revoked"
        elif agent_status == "Unknown":
            status_desc = "unregistered / unknown"
        else:
            status_desc = f"inactive ({agent_status})"

        return (
            "BLOCK",
            "R1",
            f"Agent '{agent}' is {status_desc}. Access blocked. External AI agents must be registered and active."
        )

    # -------------------------------------------------------------
    # Step 2: Amount Validation for Purchase and Refund
    # -------------------------------------------------------------
    if action in ["Place order", "Request a refund"] and amount <= 0:
        return (
            "BLOCK",
            "R7",
            f"Zero or negative amount (₹{amount:,.2f}) is invalid for '{action}'. Request blocked."
        )

    # -------------------------------------------------------------
    # Step 3: Action-Specific Rules
    # -------------------------------------------------------------
    if action == "View order":
        return (
            "ALLOW",
            "R2",
            "Registered active agent is permitted to view order history (read-only action)."
        )

    elif action == "Place order":
        if amount <= ORDER_AUTO_APPROVAL_THRESHOLD:
            return (
                "ALLOW",
                "R3",
                f"Order amount of ₹{amount:,.2f} is within the prototype auto-approval threshold of ₹{ORDER_AUTO_APPROVAL_THRESHOLD:,.0f}."
            )
        else:
            return (
                "ASK CUSTOMER",
                "R4",
                f"Order amount of ₹{amount:,.2f} exceeds the prototype limit of ₹{ORDER_AUTO_APPROVAL_THRESHOLD:,.0f}. Customer confirmation required."
            )

    elif action == "Return an order":
        return (
            "ASK CUSTOMER",
            "R5",
            "Customer must verify Nykaa's return conditions, including the 15-day return window, intact packaging, and required evidence."
        )

    elif action == "Request a refund":
        return (
            "ASK CUSTOMER",
            "R6",
            f"Direct refund request of ₹{amount:,.2f} requires customer verification and authorization."
        )

    # Fallback for unexpected action inputs
    return (
        "BLOCK",
        "R-UNKNOWN",
        f"Unsupported action '{action}'. Request blocked."
    )
