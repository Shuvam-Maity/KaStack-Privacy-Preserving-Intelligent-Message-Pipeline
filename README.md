# Privacy-Preserving Intelligent Message Pipeline

A privacy-first AI/ML message processing system designed to classify chronological messages, extract actionable tasks and events, and automatically detect and mask sensitive personally identifiable information (PII) and security credentials.

---

## ?? Key Features

1. **Part 1: Message Classification**
   - Categorizes raw messages into 6 mandatory types: \ction_required\, \meeting_or_event\, \personal_information\, \general_information\, \promotional\, or \sensitive_information\.
   - Computes deterministic confidence scores (0.0 to 1.0) and provides concise explanations for each prediction.

2. **Part 2: Task & Event Extraction**
   - Extracts structured tasks, deadlines, event details, assignees, and priority levels using \spaCy\ Named Entity Recognition (NER) and \dateparser\.
   - **Zero-Hallucination Guardrail:** Strict logic maps ambiguous or missing deadlines, times, and assignees directly to \
ull\ or unresolved states rather than fabricating values.

3. **Part 3: Sensitive Information Detection & Masking**
   - Identifies high-risk patterns including One-Time Passwords (OTPs), bank/payment details, bearer tokens, API keys, and passwords.
   - Applies string redaction (\*\) to sensitive substrings across outputs, logs, and UI components.
   - Outputs a security audit log with risk assessments (\critical\, \high\) and recommended actions (\do_not_store\, \do_not_send_to_external_service\).

---

## ??? Architecture & Pipeline Flow

\\\	ext
Raw Input Messages (CSV)
         ¦
         ?
+------------------------------+
¦  Stage 1: PII Masking & Audit¦ --? output/sensitive_info_audit.json
+------------------------------+
               ¦ (Masked Text)
               ?
+------------------------------+
¦  Stage 2: Classification     ¦ --? output/classification_results.json
+------------------------------+
               ¦
               ?
+------------------------------+
¦  Stage 3: Task/Event Extraction¦ --? output/extracted_tasks.json
+------------------------------+
\\\

---

## ?? Repository Structure

\\\	ext
KaStack-Privacy-Preserving-Intelligent-Message-Pipeline/
+-- .gitignore                  # Excludes raw CSV datasets and virtual environments
+-- README.md                   # System documentation and assignment details
+-- requirements.txt            # Dependencies and explicit SpaCy model wheel link
+-- app.py                      # Interactive Streamlit Cloud web dashboard
+-- pipeline.py                 # Core processing logic, NLP functions, and Regex patterns
+-- run_stage1_masking.py       # Stage 1 execution runner
+-- run_stage2_classify.py      # Stage 2 execution runner
+-- run_stage3_extraction.py    # Stage 3 execution runner
+-- run_all.py                  # Master runner for end-to-end processing
+-- data/
¦   +-- .gitkeep                # Retains directory structure (raw CSVs git-ignored)
+-- output/                     # Generated structured JSON deliverables
    +-- classification_results.json
    +-- extracted_tasks.json
    +-- sensitive_info_audit.json
\\\

---

## ?? Setup & Execution Guide

### Local Installation

1. Clone the repository:
   \\\ash
   git clone https://github.com/Shuvam-Maity/KaStack-Privacy-Preserving-Intelligent-Message-Pipeline.git
   cd KaStack-Privacy-Preserving-Intelligent-Message-Pipeline
   \\\

2. Activate virtual environment and install dependencies:
   \\\powershell
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   \\\

### Execution Options

* **Run End-to-End Pipeline:**
  \\\ash
  python run_all.py
  \\\

* **Run Stages Individually:**
  \\\ash
  python run_stage1_masking.py
  python run_stage2_classify.py
  python run_stage3_extraction.py
  \\\

* **Launch Interactive Web App:**
  \\\ash
  streamlit run app.py
  \\\

---

## ?? JSON Deliverables Schema

* **\output/classification_results.json\**: Contains message ID, predicted category, confidence score, and classification rationale.
* **\output/extracted_tasks.json\**: Contains structured task/event title, normalized deadline (\YYYY-MM-DD\), time, assignee, priority, and source message reference.
* **\output/sensitive_info_audit.json\**: Contains sensitivity type, risk classification, masked preview text, and security recommendation.

---

## ?? Assumptions & Security Limitations

- **Dataset Privacy:** Original CSV files (\messages.csv\, \mandatory_demo_ids.csv\) are strictly excluded from public tracking via \.gitignore\ to comply with assignment security guidelines.
- **Relative Date Context:** Relative time expressions (e.g., "tomorrow at 5 PM") depend on the local execution date provided by \dateparser\.
- **Heuristic Boundaries:** Non-standard or heavily obfuscated tokens may require specialized NER fine-tuning beyond regex heuristics.

---

## ?? AI Development Disclosure

In accordance with evaluation guidelines, AI development tools (ChatGPT / Claude) were used for assistance with boilerplate code structure, regular expression optimizations, and documentation formatting. All architectural decisions, NLP pipelines, and verification steps were implemented and validated independently.
