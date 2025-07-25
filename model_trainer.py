# model_trainer.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# 1️⃣ Load merged dataset
df = pd.read_csv("symptom_disease.csv")

# 2️⃣ Features and label
X = df.drop("prognosis", axis=1)   # All symptom columns
y = df["prognosis"]                # Disease column

# 3️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4️⃣ Train the model (with probability output)
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# 5️⃣ Evaluate model
y_pred = model.predict(X_test)
print("✅ Model Evaluation:\n")
print(classification_report(y_test, y_pred))

# 6️⃣ Save model & symptom list
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/disease_model.pkl")
joblib.dump(list(X.columns), "models/symptoms_list.pkl")

print("\n🎯 Model trained successfully and saved to models/disease_model.pkl")
print("✅ Total Symptoms:", len(X.columns))
print("✅ Total Diseases:", len(y.unique()))

