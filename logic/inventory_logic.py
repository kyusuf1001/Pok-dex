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

    return False  # Not enough keys


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


# -------------------- Using Potions --------------------

def use_heal_potion(username, pokemon_name, heal_amount=20):
    """
    Used during battles.
    Heal a specific Pokémon.
    """
    users = load_users()
    username = username.lower()

    # Check potion amount
    if users[username]["inventory"]["potions"]["heal"] <= 0:
        return False, "No healing potions left."

    # Find Pokémon
    for p in users[username]["pokemon"]:
        if p["name"].lower() == pokemon_name.lower():
            p["hp"] = min(p["max_hp"], p["hp"] + heal_amount)
            users[username]["inventory"]["potions"]["heal"] -= 1
            save_users(users)
            return True, f"{pokemon_name} healed for {heal_amount} HP!"

    return False, "Pokémon not found."


def use_xp_potion(username, amount=20):
    """
    Gives XP directly.
    """
    users = load_users()
    username = username.lower()

    if users[username]["inventory"]["potions"]["xp"] <= 0:
        return False, "No XP potions left."

    users[username]["xp"] += amount
    users[username]["inventory"]["potions"]["xp"] -= 1
    save_users(users)

    return True, f"Gained {amount} XP!"
