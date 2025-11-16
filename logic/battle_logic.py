import json
import os
from logic.inventory_logic import load_users, save_users, remove_potion

DATA_PATH = os.path.join("data", "users.json")

RARITY_REWARDS = {
    "common": {"xp": 5, "money": 5},
    "rare": {"xp": 12, "money": 12},
    "epic": {"xp": 20, "money": 20},
    "mythic": {"xp": 30, "money": 30},
    "legendary": {"xp": 50, "money": 50}
}

def apply_damage(username, amount):
    users = load_users()
    username = username.lower()

    p = users[username]["active_pokemon"]
    if not p:
        return False, "No active Pokémon!"

    p["hp"] = max(0, p["hp"] - amount)
    save_users(users)

    return True, f"{p['name']} took {amount} damage!"


def heal_active(username, amount):
    users = load_users()
    username = username.lower()

    p = users[username]["active_pokemon"]
    if not p:
        return False, "No active Pokémon!"

    if not remove_potion(users, username, "heal", 1):
        return False, "No healing potions left."

    p["hp"] = min(p["max_hp"], p["hp"] + amount)
    save_users(users)

    return True, f"{p['name']} healed for {amount}!"


def reward_for_win(username, rarity):
    users = load_users()
    username = username.lower()

    if rarity not in RARITY_REWARDS:
        return False, "Invalid rarity."

    users[username]["xp"] += RARITY_REWARDS[rarity]["xp"]
    users[username]["money"] += RARITY_REWARDS[rarity]["money"]

    save_users(users)

    return True, f"Victory! You earned rewards from a {rarity} Pokémon."
