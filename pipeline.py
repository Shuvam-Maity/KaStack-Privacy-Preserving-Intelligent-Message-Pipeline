import re
import json
import pandas as pd
import spacy
import dateparser
from typing import Dict, Any, List, Tuple, Optional

# Load SpaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# --- PART 3: SENSITIVE INFO DETECTION PATTERNS ---
PATTERNS = {
    "one_time_password": [
        (r'\b(?:otp|one[- ]time[- ]password|code)\b.*?(\b\d{4,8}\b)', "high", "do_not_store"),
    ],
    "password_credentials": [
        (r'(?i)\b(?:password|passcode|pwd)\s*[:=]\s*(\S+)', "critical", "do_not_store"),
    ],
    "bank_payment_details": [
        (r'\b(?:\d[ -]*?){13,16}\b', "critical", "do_not_store"),
    ],
    "authentication_token": [
        (r'\b(bearer\s+[A-Za-z0-9\-\._~\+\/]+=*)', "critical", "do_not_send_to_external_service"),
        (r'\b(api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]{16,})\b', "critical", "do_not_send_to_external_service")
    ]
}

def detect_and_mask(message: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Detects sensitive details and masks matching text."""
    masked_text = message
    detected_info = None

    for sens_type, rule_list in PATTERNS.items():
        for pattern, risk, action in rule_list:
            matches = list(re.finditer(pattern, message, re.IGNORECASE))
            if matches:
                if not detected_info:
                    detected_info = {
                        "sensitivity_type": sens_type,
                        "risk": risk,
                        "recommended_action": action
                    }
                for match in matches:
                    val = match.group(0)
                    masked_text = masked_text.replace(val, "*" * len(val))

    return detected_info, masked_text

# --- PART 1: MESSAGE CLASSIFICATION ---
def classify_message(message: str, is_sensitive: bool) -> Dict[str, Any]:
    """Classifies a message into one of the six designated categories."""
    if is_sensitive:
        return {
            "category": "sensitive_information",
            "confidence": 0.98,
            "reason": "Detected confidential authentication or payment pattern."
        }
    
    msg_lower = message.lower()
    if any(k in msg_lower for k in ["discount", "sale", "% off", "offer", "buy now"]):
        return {"category": "promotional", "confidence": 0.92, "reason": "Commercial language detected."}
    
    if any(k in msg_lower for k in ["meet", "zoom", "schedule", "call at", "event"]):
        return {"category": "meeting_or_event", "confidence": 0.89, "reason": "Scheduling terms present."}
    
    if any(k in msg_lower for k in ["please submit", "action required", "deadline", "urgent"]):
        return {"category": "action_required", "confidence": 0.90, "reason": "Explicit action requested."}
    
    if any(k in msg_lower for k in ["my address", "my phone", "my email"]):
        return {"category": "personal_information", "confidence": 0.85, "reason": "Non-sensitive personal details present."}

    return {"category": "general_information", "confidence": 0.80, "reason": "Standard informational context."}

# --- PART 2: TASK & EVENT EXTRACTION ---
def extract_task_or_event(msg_id: str, message: str, category: str) -> Optional[Dict[str, Any]]:
    """Extracts tasks and events without guessing missing values."""
    if category not in ["action_required", "meeting_or_event"]:
        return None

    doc = nlp(message)
    dates = [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]
    people = [ent.text for ent in doc.ents if ent.label_ in ["PERSON"]]

    parsed_date, parsed_time = None, None
    if dates:
        dt = dateparser.parse(dates[0], settings={'PREFER_DATES_FROM': 'future'})
        if dt:
            parsed_date = dt.strftime("%Y-%m-%d")
            if dt.strftime("%H:%M:%S") != "00:00:00":
                parsed_time = dt.strftime("%H:%M")

    priority = "high" if any(w in message.lower() for w in ["urgent", "asap", "critical"]) else "medium"
    item_type = "event" if category == "meeting_or_event" else "task"

    return {
        "item_id": f"{'EVENT' if item_type == 'event' else 'TASK'}_{msg_id}",
        "type": item_type,
        "title": message[:50] + ("..." if len(message) > 50 else ""),
        "deadline": parsed_date if item_type == "task" else None,
        "time": parsed_time,
        "person": people[0] if people else None,
        "priority": priority,
        "source_message_id": msg_id
    }