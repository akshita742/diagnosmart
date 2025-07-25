# merge_dataset.py

import pandas as pd

# Load Kaggle CSVs
train = pd.read_csv("Training.csv")
test = pd.read_csv("Testing.csv")

# Drop extra empty column (Unnamed: 133)
train = train.drop(columns=["Unnamed: 133"], errors="ignore")
test = test.drop(columns=["Unnamed: 133"], errors="ignore")

# Combine both datasets
full_df = pd.concat([train, test], ignore_index=True)

# Save a single master dataset
full_df.to_csv("symptom_disease.csv", index=False)

print("✅ Combined dataset saved as symptom_disease.csv")
print(f"📊 Total rows: {full_df.shape[0]} | Total columns: {full_df.shape[1]}")
