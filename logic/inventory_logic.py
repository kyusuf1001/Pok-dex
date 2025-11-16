import json
import os

DATA_PATH = os.path.join("data", "users.json")

# -------------------- Load & Save --------------------

def load_users():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

# -------------------- Inventory Functions --------------------

def get_inventory(username):
    users = load_users()
    username = username.lower()
    return users[username]["inventory"]

# ---- KEY FUNCTIONS ----

def add_key(username, key_type, amount=1):
    users = load_users()
    username = username.lower()

    users[username]["inventory"]["keys"][key_type] += amount
    save_users(users)

def remove_key(username, key_type, amount=1):
    users = load_users()
    username = username.lower()

    if users[username]["inventory"]["keys"][key_type] >= amount:
        users[username]["inventory"]["keys"][key_type] -= amount
        save_users(users)
        return True

    return False

# ---- POTION FUNCTIONS ----

def add_potion(username, potion_type, amount=1):
    users = load_users()
    username = username.lower()

    users[username]["inventory"]["potions"][potion_type] += amount
    save_users(users)

def remove_potion(username, potion_type, amount=1):
    users = load_users()
    username = username.lower()

    if users[username]["inventory"]["potions"][potion_type] >= amount:
        users[username]["inventory"]["potions"][potion_type] -= amount
        save_users(users)
        return True

    return False
