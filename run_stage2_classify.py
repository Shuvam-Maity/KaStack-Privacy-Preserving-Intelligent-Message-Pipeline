import os
import json
import pandas as pd
from pipeline import classify_message

def main():
    print("--- Stage 2: Message Classification ---")
    os.makedirs("output", exist_ok=True)

    df_masked = pd.read_csv("data/masked_messages_temp.csv")
    df_mandatory = pd.read_csv("data/mandatory_demo_ids.csv")
    
    # Normalize mandatory demo IDs
    df_mandatory.columns = df_mandatory.columns.str.strip().str.lower().str.replace(' ', '_')
    mand_col = 'message_id' if 'message_id' in df_mandatory.columns else df_mandatory.columns[0]
    mandatory_ids = set(df_mandatory[mand_col].astype(str))

    classification_results = []

    for _, row in df_masked.iterrows():
        msg_id = str(row['Message ID'])
        text = str(row['Masked Message'])
        is_sensitive = bool(row['Is Sensitive'])
        
        res = classify_message(text, is_sensitive)
        
        classification_results.append({
            "message_id": msg_id,
            "category": res["category"],
            "confidence": res["confidence"],
            "reason": res["reason"]
        })

    with open("output/classification_results.json", "w") as f:
        json.dump(classification_results, f, indent=2)

    print(f"Classified {len(classification_results)} messages.")
    
    df_results = pd.DataFrame(classification_results)
    mandatory_matches = df_results[df_results['message_id'].isin(mandatory_ids)]
    print(f"Verified {len(mandatory_matches)} / {len(mandatory_ids)} mandatory demo IDs.")
    print("Saved classification results to: output/classification_results.json\n")

if __name__ == "__main__":
    main()