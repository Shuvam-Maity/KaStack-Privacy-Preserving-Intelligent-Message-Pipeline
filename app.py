import streamlit as st
import pandas as pd
import json
from pipeline import detect_and_mask, classify_message, extract_task_or_event

st.set_page_config(page_title="AI Message Processing System", layout="wide")
st.title("🛡️ Privacy-Preserving Intelligent Message Pipeline")

uploaded_file = st.file_uploader("Upload Assignment CSV Dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.info(f"Loaded {len(df)} messages.")

    if st.button("Run Processing Pipeline"):
        classifications, tasks, sensitivities = [], [], []

        for _, row in df.iterrows():
            msg_id = str(row.get('Message ID', row.get('message_id', '')))
            raw_msg = str(row.get('Message', row.get('message', '')))

            sens_info, masked_text = detect_and_mask(raw_msg)
            if sens_info:
                sensitivities.append({
                    "message_id": msg_id,
                    "sensitivity_type": sens_info["sensitivity_type"],
                    "risk": sens_info["risk"],
                    "masked_text": masked_text,
                    "recommended_action": sens_info["recommended_action"]
                })

            class_res = classify_message(masked_text, sens_info is not None)
            classifications.append({
                "message_id": msg_id,
                "category": class_res["category"],
                "confidence": class_res["confidence"],
                "reason": class_res["reason"]
            })

            task_res = extract_task_or_event(msg_id, masked_text, class_res["category"])
            if task_res:
                tasks.append(task_res)

        st.session_state["done"] = True
        st.session_state["class_res"] = classifications
        st.session_state["tasks_res"] = tasks
        st.session_state["sens_res"] = sensitivities

if st.session_state.get("done"):
    tab1, tab2, tab3 = st.tabs(["Classifications", "Extracted Tasks & Events", "Sensitive Data Log"])
    with tab1:
        st.dataframe(pd.DataFrame(st.session_state["class_res"]))
    with tab2:
        st.dataframe(pd.DataFrame(st.session_state["tasks_res"]))
    with tab3:
        st.json(st.session_state["sens_res"])