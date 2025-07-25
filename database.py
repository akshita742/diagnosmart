# database.py

import sqlite3
import json
from datetime import datetime

DB_NAME = "diagnoser.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  symptoms TEXT,
                  predicted_disease TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def insert_prediction(symptoms_dict, predicted_disease):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO predictions (symptoms, predicted_disease, timestamp) VALUES (?, ?, ?)",
              (json.dumps(symptoms_dict), predicted_disease, datetime.now()))
    conn.commit()
    conn.close()

# ✅ NEW: Fetch all predictions
def fetch_predictions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data
