import os
import json
import pandas as pd
from pipeline import detect_and_mask

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strips whitespace and converts column names to standard keys."""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def main():
    print("--- Stage 1: Sensitive Information Detection & Masking ---")
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    df_raw = pd.read_csv("data/messages.csv")
    df_raw = normalize_columns(df_raw)
    print(f"Loaded {len(df_raw)} raw messages.")

    # Determine column names dynamically
    id_col = 'message_id' if 'message_id' in df_raw.columns else df_raw.columns[0]
    msg_col = 'message' if 'message' in df_raw.columns else df_raw.columns[-1]
    timestamp_col = 'timestamp' if 'timestamp' in df_raw.columns else None
    sender_col = 'sender' if 'sender' in df_raw.columns else None

    sensitivity_logs = []
    masked_messages = []

    for _, row in df_raw.iterrows():
        msg_id = str(row[id_col])
        raw_text = str(row[msg_col])
        
        sens_info, masked_text = detect_and_mask(raw_text)
        
        masked_messages.append({
            "Message ID": msg_id,
            "Timestamp": row[timestamp_col] if timestamp_col else None,
            "Sender": row[sender_col] if sender_col else None,
            "Masked Message": masked_text,
            "Is Sensitive": sens_info is not None
        })
        
        if sens_info:
            sensitivity_logs.append({
                "message_id": msg_id,
                "sensitivity_type": sens_info["sensitivity_type"],
                "risk": sens_info["risk"],
                "masked_text": masked_text,
                "recommended_action": sens_info["recommended_action"]
            })

    pd.DataFrame(masked_messages).to_csv("data/masked_messages_temp.csv", index=False)
    with open("output/sensitive_info_audit.json", "w") as f:
        json.dump(sensitivity_logs, f, indent=2)

    print(f"Detected {len(sensitivity_logs)} sensitive entries.")
    print("Saved audit to: output/sensitive_info_audit.json\n")

if __name__ == "__main__":
    main()