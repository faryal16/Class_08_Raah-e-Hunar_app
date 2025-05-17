import json
import os

DATA_FILE = "workshop_enrollments.json"

def load_enrollments():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_enrollments(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user_workshops(email):
    data = load_enrollments()
    return data.get(email, [])

def add_user_workshop(email, workshop):
    data = load_enrollments()
    user_workshops = data.get(email, [])
     # If user has no free workshop yet and this one is free, mark it
    if workshop["price"] == 0 and not any(w.get("free_first", False) for w in user_workshops):
        workshop["free_first"] = True
    # avoid duplicates
    if not any(w["title"] == workshop["title"] for w in user_workshops):
        user_workshops.append(workshop)
    data[email] = user_workshops
    save_enrollments(data)
