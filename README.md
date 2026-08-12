# Privacy-Preserving Intelligent Message Pipeline

A robust, privacy-first AI/ML processing pipeline designed to classify raw chronological messages, extract actionable tasks and event details, and detect/mask sensitive personally identifiable information (PII) or secrets.

---

## 🌟 Overview & Features

This system processes unstructured communication data locally and in real time through three decoupled stages:

1. **Part 1: Message Classification**
   - Categorizes each input message into one of 6 mandatory categories: `action_required`, `meeting_or_event`, `personal_information`, `general_information`, `promotional`, or `sensitive_information`.
   - Computes a confidence score (0.0 to 1.0) and generates a brief human-readable explanation for each prediction.

2. **Part 2: Task and Event Extraction**
   - Extracts structured tasks, deadlines, event details, assignees, and priorities using `spaCy` Named Entity Recognition (NER) and `dateparser`.
   - **Zero Hallucination Guardrail:** Strict logic maps ambiguous or missing deadlines, times, and assignees directly to `null` or unresolved states rather than fabricating values.

3. **Part 3: Sensitive Information Detection & Masking**
   - Identifies high-risk patterns including One-Time Passwords (OTPs), bank/payment credentials, bearer tokens, API keys, and account passwords.
   - Applies redaction (asterisks `*`) to sensitive text substrings before passing messages to classification layers, output files, logs, or UI displays.
   - Provides risk assessments (`critical`, `high`) and actionable security guidelines (`do_not_store`, `do_not_send_to_external_service`).

---

## 🏗️ How the Pipeline Works

### 1. Classification Methodology
- **Pre-Masking Input:** Messages first pass through the PII masking layer. If sensitive authentication or financial patterns are detected, the message is prioritized as `sensitive_information` with high confidence.
- **Contextual Categorization:** Evaluates linguistic cues, urgency phrases, commercial language, and scheduling terminology.
- **Deterministic Confidence:** Assigns scores based on rule context strength and semantic pattern matches.

### 2. Task & Event Extraction Logic
- **Entity Parsing:** Uses `spaCy` (`en_core_web_sm`) to extract `DATE`, `TIME`, and `PERSON` entities from actionable messages (`action_required` and `meeting_or_event`).
- **Date Normalization:** Converts relative and absolute date strings into standardized `YYYY-MM-DD` and `HH:MM` formats via `dateparser`.
- **Field Safety:** If an entity is absent or ambiguous in the source text, the property remains `null`.

### 3. Sensitive Data Masking Mechanics
- **Pattern Matching:** Utilizes regex rules tuned for credit cards, tokens, passwords, and verification codes.
- **Data Protection:** Redacts matching substrings directly at string boundaries before downstream processing, ensuring raw credentials never appear in output JSON files, Streamlit UI components, or cloud logs.

---

## 📁 Repository Structure

```text
kastack-message-intelligence/
├── .gitignore                  # Prevents raw CSV dataset files from being committed
├── README.md                   # System documentation and assignment breakdown
├── requirements.txt            # Environment dependencies and SpaCy model wheels
├── app.py                      # Interactive Streamlit Cloud web interface
├── pipeline.py                 # Core business logic and shared NLP functions
├── run_stage1_masking.py       # Stage 1: PII Detection & Security Audit
├── run_stage2_classify.py      # Stage 2: Category Predictions & Mandatory ID Check
├── run_stage3_extraction.py    # Stage 3: Task & Event Structuring
├── run_all.py                  # End-to-end master pipeline runner
├── data/
│   └── .gitkeep                # Tracks local folder in Git (raw CSVs remain git-ignored)
└── output/                     # Generated structured output JSON files
    ├── classification_results.json
    ├── extracted_tasks.json
    └── sensitive_info_audit.json
