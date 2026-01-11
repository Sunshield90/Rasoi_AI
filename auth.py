import streamlit as st
import hashlib
import json
import os

# Database file to store users
DB_FILE = "users_db.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def signup(username, password):
    init_db()
    with open(DB_FILE, "r") as f:
        users = json.load(f)
    
    if username in users:
        return False, "User already exists!"
    
    users[username] = hash_password(password)
    
    with open(DB_FILE, "w") as f:
        json.dump(users, f)
        
    return True, "Account created! Please log in."

def login(username, password):
    init_db()
    with open(DB_FILE, "r") as f:
        users = json.load(f)
    
    if username not in users:
        return False
        
    if users[username] == hash_password(password):
        return True
    
    return False