# Privacy-Preserving Intelligent Message Pipeline

A robust, privacy-first AI/ML processing pipeline designed to classify raw chronological messages, extract actionable tasks and event details, and detect/mask sensitive personally identifiable information (PII) or security credentials.

---

## 🔗 Project & Submission Links

* **Live Cloud-Hosted Web App:** [KaStack Intelligent Message Pipeline](https://kastack-privacy-preserving-intelligent-message-pipeline.streamlit.app/)
* **Video Demonstration (Loom):** [Watch System Walkthrough](https://www.loom.com/share/73f28609bf174101b279cdb4a15e24f)
* **GitHub Repository:** [Shuvam-Maity/KaStack-Privacy-Preserving-Intelligent-Message-Pipeline](https://github.com/Shuvam-Maity/KaStack-Privacy-Preserving-Intelligent-Message-Pipeline)

---

## 🌟 Overview

The **Privacy-Preserving Intelligent Message Pipeline** is an end-to-end NLP pipeline that processes unstructured chronological messages while prioritizing privacy and security.

The system performs three decoupled stages:

1. **PII & Sensitive Information Detection/Masking**
2. **Message Classification**
3. **Task & Event Extraction**

Raw sensitive information is masked before downstream processing, preventing credentials and other secrets from being exposed in later processing stages, application views, or generated logs.

---

## 🏗️ System Architecture

```text
Raw Input Messages (CSV)
         │
         ▼
┌─────────────────────────────────┐
│ Stage 1: PII Masking & Audit    │
│                                 │
│ • Detect sensitive information  │
│ • Mask credentials              │
│ • Generate security audit       │
└───────────────┬─────────────────┘
                │
                │ Masked Text
                ▼
┌─────────────────────────────────┐
│ Stage 2: Message Classification │
│                                 │
│ • Categorize messages           │
│ • Calculate confidence           │
│ • Generate rationale             │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│ Stage 3: Task/Event Extraction   │
│                                 │
│ • Extract entities               │
│ • Normalize dates/times          │
│ • Extract tasks and events       │
└─────────────────────────────────┘
```

### Pipeline Outputs

```text
output/
├── sensitive_info_audit.json
├── classification_results.json
└── extracted_tasks.json
```

---

# 🛠️ Pipeline Design & Core Mechanics

## 1. Sensitive Information Detection & Masking

The first stage ensures that sensitive information is identified and removed before the message reaches downstream processing.

### Pattern Matching Engine

The pipeline uses carefully designed regular expressions to detect sensitive information such as:

* One-Time Passwords (OTPs)
* Payment card numbers
* API keys
* Bearer tokens
* Account passwords
* Authentication credentials

### String Boundary Redaction

Detected secrets are replaced with asterisks (`*`) before the message is passed to subsequent stages.

This ensures that raw credentials are not exposed through:

* Classification processing
* Task/event extraction
* Streamlit UI views
* Generated JSON outputs
* Secondary processing stages

### Security Audit Logging

Detected sensitive information is recorded separately in:

```text
output/sensitive_info_audit.json
```

The audit records include:

* Sensitivity type
* Risk level
* Masked preview
* Recommended security action

Example recommendations include:

```text
do_not_store
do_not_send_to_external_service
```

---

# 2. Message Classification

Stage 2 operates exclusively on the **masked message output** from Stage 1.

Messages are classified into six mandatory categories:

```text
action_required
meeting_or_event
personal_information
general_information
promotional
sensitive_information
```

### Classification Logic

The classifier evaluates:

* Linguistic cues
* Action-oriented terminology
* Urgency markers
* Scheduling terminology
* Sensitive-information indicators
* Message context

Messages containing detected authentication credentials or sensitive security patterns are prioritized as:

```text
sensitive_information
```

### Deterministic Confidence & Rationales

Each classification produces:

* Predicted category
* Confidence score between `0.0` and `1.0`
* Human-readable rationale

This makes the classification process transparent and easier to audit.

---

# 3. Task & Event Extraction

The third stage extracts structured tasks and events from actionable messages.

Task/event extraction is primarily performed for:

```text
action_required
meeting_or_event
```

### Named Entity Recognition

The pipeline uses **spaCy** with:

```text
en_core_web_sm
```

to identify entities such as:

* `DATE`
* `TIME`
* `PERSON`

### Date & Time Normalization

The pipeline uses **dateparser** to convert both relative and absolute date/time expressions into standardized formats.

Examples:

```text
YYYY-MM-DD
HH:MM
```

For example:

```text
tomorrow at 5 PM
```

can be normalized into a structured date and time representation based on the execution context.

### Zero-Hallucination Guardrail

The extraction pipeline does **not invent missing information**.

If a property such as:

* Deadline
* Time
* Assignee
* Event information

is missing or ambiguous, the system explicitly returns:

```text
null
```

instead of generating an artificial value.

This ensures that extracted structured data remains grounded in the original message.

---

# 📁 Repository Structure

```text
KaStack-Privacy-Preserving-Intelligent-Message-Pipeline/
│
├── data/
│   └── .gitkeep
│
├── output/
│   ├── classification_results.json
│   ├── extracted_tasks.json
│   └── sensitive_info_audit.json
│
├── .gitignore
├── README.md
├── app.py
├── pipeline.py
├── requirements.txt
├── run_all.py
├── run_stage1_masking.py
├── run_stage2_classify.py
└── run_stage3_extraction.py
```

---

# 📌 Generated Structured Output Files

All processed information is stored in structured JSON format inside the `output/` directory.

## `classification_results.json`

Contains:

* Message ID
* Predicted category
* Confidence score
* Classification rationale

---

## `extracted_tasks.json`

Contains structured task/event information such as:

* Task/event title
* Normalized deadline
* Time
* Assignee
* Priority
* Source message reference

---

## `sensitive_info_audit.json`

Contains:

* Sensitive information type
* Risk classification
* Masked text preview
* Security recommendations

---

# 🚀 Setup & Execution

## Prerequisites

Make sure Python is installed on your system.

---

## 1. Clone the Repository

```bash
git clone https://github.com/Shuvam-Maity/KaStack-Privacy-Preserving-Intelligent-Message-Pipeline.git
cd KaStack-Privacy-Preserving-Intelligent-Message-Pipeline
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Execution

## Run the Complete Pipeline

Execute all three stages sequentially:

```bash
python run_all.py
```

---

## Run Individual Stages

### Stage 1 — PII & Sensitive Information Masking

```bash
python run_stage1_masking.py
```

### Stage 2 — Message Classification

```bash
python run_stage2_classify.py
```

### Stage 3 — Task/Event Extraction

```bash
python run_stage3_extraction.py
```

---

# 🖥️ Launch the Streamlit Application

To launch the interactive web application locally:

```bash
streamlit run app.py
```

The application provides an interactive interface for processing and inspecting the pipeline results.

---

# 🔐 Privacy & Security Design

Privacy is treated as a core architectural requirement rather than an additional post-processing step.

The pipeline follows a **mask-before-processing** strategy:

```text
Raw Message
     │
     ▼
Sensitive Information Detection
     │
     ▼
Credential/PII Masking
     │
     ▼
Masked Message
     │
     ├──► Classification
     │
     └──► Task/Event Extraction
```

This design minimizes the possibility of sensitive credentials being propagated into downstream components.

Raw datasets are also excluded from version control.

---

# ⚠️ Assumptions & Limitations

## Dataset Privacy

Raw CSV datasets such as:

```text
messages.csv
mandatory_demo_ids.csv
```

are intentionally excluded from public tracking through `.gitignore` to comply with data privacy requirements.

---

## Relative Date Context

Relative date expressions such as:

```text
tomorrow at 5 PM
next Monday
this Friday
```

depend on the local execution date/context supplied to `dateparser`.

Therefore, the same relative expression may produce different normalized dates when executed on different days.

---

## Pattern-Based Secret Detection

The sensitive-information detection system relies primarily on regex-based pattern matching.

Highly obfuscated, fragmented, or non-standard secret formats may not be detected and could require:

* Specialized NER models
* Machine-learning-based detection
* Custom entity recognition
* Additional security rules

---

# 🤖 AI-Tool Usage Declaration

In accordance with the assignment guidelines, AI development assistants including **ChatGPT** and **Claude** were used for:

* Boilerplate code setup
* Regular expression optimization
* Documentation formatting
* Development assistance

All major architectural decisions, NLP logic, pipeline orchestration, and output validation steps were independently designed, implemented, tested, and verified.

---

# 🌐 Live Demo

**Web Application:**
https://kastack-privacy-preserving-intelligent-message-pipeline.streamlit.app/

**Video Walkthrough:**
https://www.loom.com/share/73f28609bf174101b279cdb4a15e24f

**Source Code:**
https://github.com/Shuvam-Maity/KaStack-Privacy-Preserving-Intelligent-Message-Pipeline

---

## 📄 License

This project is intended for educational, demonstration, and assignment purposes.
