# predictor.py

import joblib
import numpy as np

# Load model and symptom list
model = joblib.load("models/disease_model.pkl")
SYMPTOMS = joblib.load("models/symptoms_list.pkl")

def predict_disease_with_confidence(user_input: dict, top_k=3):
    """
    Takes a dictionary of symptoms like {'fever': 1, 'headache': 0, ...}
    Returns top_k diseases with confidence scores
    """
    # Arrange inputs in correct order
    input_vec = [user_input.get(symptom, 0) for symptom in SYMPTOMS]

    # Get prediction probabilities
    proba = model.predict_proba([input_vec])[0]

    # Sort probabilities descending
    top_indices = np.argsort(proba)[::-1][:top_k]

    results = []
    for idx in top_indices:
        disease = model.classes_[idx]
        confidence = round(proba[idx] * 100, 2)  # convert to %
        results.append((disease, confidence))

    return results

# ✅ Test example (delete later)
if __name__ == "__main__":
    # Fake symptom input for testing
    sample_input = {sym: 0 for sym in SYMPTOMS}
    sample_input['headache'] = 1
    sample_input['fever'] = 1
    sample_input['nausea'] = 1

    print(predict_disease_with_confidence(sample_input))

