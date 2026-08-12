import os
import json
import pandas as pd
from pipeline import extract_task_or_event

def main():
    print("--- Stage 3: Task & Event Extraction ---")
    os.makedirs("output", exist_ok=True)

    df_masked = pd.read_csv("data/masked_messages_temp.csv")
    
    with open("output/classification_results.json", "r") as f:
        classifications = json.load(f)

    category_map = {item["message_id"]: item["category"] for item in classifications}
    extracted_items = []

    for _, row in df_masked.iterrows():
        msg_id = str(row['Message ID'])
        text = str(row['Masked Message'])
        category = category_map.get(msg_id, "general_information")
        
        item = extract_task_or_event(msg_id, text, category)
        if item:
            extracted_items.append(item)

    with open("output/extracted_tasks.json", "w") as f:
        json.dump(extracted_items, f, indent=2)

    print(f"Extracted {len(extracted_items)} actionable items.")
    print("Saved extracted tasks to: output/extracted_tasks.json\n")

if __name__ == "__main__":
    main()