import json
import os
from logic.inventory_logic import load_users, save_users

DATA_PATH = os.path.join("data", "users.json")


# -------------------- Damage Handling --------------------

def apply_damage(username, amount):
    """Subtract HP from the active Pokémon."""
    username = username.lower()
    users = load_users()

    active_name = users[username]["active_pokemon"]
    if not active_name:
        return False, "No active Pokémon selected."

    # Find Pokémon
    for p in users[username]["pokemon"]:
        if p["name"] == active_name:
            p["hp"] = max(0, p["hp"] - amount)
            save_users(users)
            return True, f"{active_name} took {amount} damage. New HP: {p['hp']}"

    return False, "Active Pokémon not found."


# -------------------- Healing --------------------

def heal_active(username, amount):
    """Heal the active Pokémon (used by potions)."""
    username = username.lower()
    users = load_users()

    active_name = users[username]["active_pokemon"]
    if not active_name:
        return False, "No active Pokémon selected."

    # Find Pokémon
    for p in users[username]["pokemon"]:
        if p["name"] == active_name:
            p["hp"] = min(p["max_hp"], p["hp"] + amount)
            save_users(users)
            return True, f"{active_name} healed for {amount}. New HP: {p['hp']}"

    return False, "Active Pokémon not found."


# -------------------- Win Rewards --------------------

RARITY_REWARDS = {
    "common":    {"xp": 10,  "money": 5},
    "rare":      {"xp": 20,  "money": 10},
    "epic":      {"xp": 40,  "money": 20},
    "mythic":    {"xp": 70,  "money": 35},
    "legendary": {"xp": 120, "money": 60}
}


def reward_for_win(username, enemy_pokemon_rarity):
    """Give XP and money for winning a real-life battle."""
    username = username.lower()
    users = load_users()

    if enemy_pokemon_rarity not in RARITY_REWARDS:
        return False, "Invalid rarity."

    reward = RARITY_REWARDS[enemy_pokemon_rarity]

    users[username]["xp"] += reward["xp"]
    users[username]["money"] += reward["money"]

    save_users(users)

    return True, f"Victory rewards: +{reward['xp']} XP, +{reward['money']} money!"
