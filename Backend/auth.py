import hashlib
import json
import os

# Database file to store users
DB_FILE = "users_db.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def load_db():
    init_db()
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_db(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def signup(username, password):
    users = load_db()
    if username in users:
        return False, "User already exists!"
    
    # Store user as a dictionary to support history storage
    users[username] = {
        "password": hash_password(password),
        "history": []
    }
    save_db(users)
    return True, "Account created! Please log in."

def login(username, password):
    users = load_db()
    if username not in users:
        return False, None
        
    stored_data = users[username]
    # Compatibility check for older string-based password storage
    stored_hash = stored_data["password"] if isinstance(stored_data, dict) else stored_data
    
    if stored_hash == hash_password(password):
        user_data = stored_data if isinstance(stored_data, dict) else {"password": stored_hash, "history": []}
        return True, user_data
    
    return False, None

def save_recipe_to_history(username, recipe_title):
    users = load_db()
    if username in users:
        # Convert legacy string data to dictionary if necessary
        if isinstance(users[username], str):
            users[username] = {"password": users[username], "history": []}
        
        if "history" not in users[username]:
            users[username]["history"] = []
            
        users[username]["history"].insert(0, recipe_title)
        users[username]["history"] = users[username]["history"][:20] # Limit to 20 items
        save_db(users)
        return True
    return False