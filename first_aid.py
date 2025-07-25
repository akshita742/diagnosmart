# first_aid.py
import json

with open("first_aid.json", "r") as f:
    first_aid_data = json.load(f)

def get_first_aid_info(disease_name: str):
    info = first_aid_data.get(disease_name)
    if info:
        return info["first_aid"], info["urgency"]
    else:
        return None, None
