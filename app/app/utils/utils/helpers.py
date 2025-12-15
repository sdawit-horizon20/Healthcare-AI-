import json
import os

DB_FILE = "db/database.json"

if not os.path.exists(DB_FILE):
    os.makedirs("db", exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    db = load_db()
    return db["users"].get(user_id, None)

def create_user(user_id):
    db = load_db()
    if user_id not in db["users"]:
        db["users"][user_id] = {"paid": False, "tier": "free", "conversation": []}
        save_db(db)

def add_message(user_id, role, content):
    db = load_db()
    create_user(user_id)
    db["users"][user_id]["conversation"].append({"role": role, "content": content})
    save_db(db)

def mark_paid(user_id):
    db = load_db()
    create_user(user_id)
    db["users"][user_id]["paid"] = True
    db["users"][user_id]["tier"] = "premium"
    save_db(db)
