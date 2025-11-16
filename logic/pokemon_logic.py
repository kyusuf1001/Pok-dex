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


# -------------------- Rarity Ranking --------------------

RARITY_ORDER = {
    "legendary": 5,
    "mythic": 4,
    "epic": 3,
    "rare": 2,
    "common": 1
}


# -------------------- Get All Pokémon --------------------

def get_pokemon_list(username):
    username = username.lower()
    users = load_users()

    pokemon_list = users[username]["pokemon"]

    # Sort: legendary > mythic > epic > rare > common
    pokemon_list = sorted(
        pokemon_list,
        key=lambda p: RARITY_ORDER.get(p["rarity"], 0),
        reverse=True
    )

    return pokemon_list


# -------------------- Get Pokémon Details --------------------

def get_pokemon(username, pokemon_name):
    username = username.lower()
    users = load_users()

    for p in users[username]["pokemon"]:
        if p["name"].lower() == pokemon_name.lower():
            return p

    return None


# -------------------- Set Active Pokémon --------------------

def set_active_pokemon(username, pokemon_name):
    username = username.lower()
    users = load_users()

    for p in users[username]["pokemon"]:
        if p["name"].lower() == pokemon_name.lower():
            users[username]["active_pokemon"] = p["name"]
            save_users(users)
            return True, f"Active Pokémon set to {p['name']}."

    return False, "Pokémon not found."


# -------------------- Get Active Pokémon --------------------

def get_active_pokemon(username):
    username = username.lower()
    users = load_users()

    active = users[username]["active_pokemon"]

    if not active:
        return None

    for p in users[username]["pokemon"]:
        if p["name"] == active:
            return p

    return None
