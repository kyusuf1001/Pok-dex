import json
import os
from logic.inventory_logic import load_users, save_users

USERS_PATH = os.path.join("data", "users.json")


# -------------------- Load Pokémon List --------------------

def get_pokemon_list(username):
    users = load_users()
    username = username.lower()
    return users[username]["pokemon"]


def get_pokemon(username, name):
    users = load_users()
    username = username.lower()

    for p in users[username]["pokemon"]:
        if p["name"].lower() == name.lower():
            return p

    return None


# -------------------- Active Pokémon --------------------

def set_active_pokemon(username, pokemon_name):
    users = load_users()
    username = username.lower()

    for p in users[username]["pokemon"]:
        if p["name"].lower() == pokemon_name.lower():
            users[username]["active_pokemon"] = p
            save_users(users)
            return True, "Active Pokémon updated!"

    return False, "Pokémon not found."


def get_active_pokemon(username):
    users = load_users()
    username = username.lower()

    return users[username]["active_pokemon"]
