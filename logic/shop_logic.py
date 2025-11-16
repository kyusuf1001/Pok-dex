import os
import json
from logic.inventory_logic import load_users, save_users, add_key, add_potion

DATA_PATH = os.path.join("data", "users.json")

KEY_PRICES = {
    "wooden": 10,
    "iron": 25,
    "gold": 50,
    "mythic": 100,
    "ultimate": 200
}

POTION_PRICES = {
    "heal": 15,
    "xp": 25
}

def buy_key(username, key_type):
    users = load_users()
    username = username.lower()

    if key_type not in KEY_PRICES:
        return False, "Invalid key type."

    cost = KEY_PRICES[key_type]
    money = users[username]["money"]

    if money < cost:
        return False, f"Not enough money. A {key_type} key costs {cost} coins."

    # Buy successful
    users[username]["money"] -= cost
    add_key(users, username, key_type, 1)
    save_users(users)

    return True, f"Bought 1 {key_type.capitalize()} Key for {cost} coins!"


def buy_potion(username, potion_type):
    users = load_users()
    username = username.lower()

    if potion_type not in POTION_PRICES:
        return False, "Invalid potion type."

    cost = POTION_PRICES[potion_type]
    money = users[username]["money"]

    if money < cost:
        return False, f"Not enough money. A {potion_type.capitalize()} Potion costs {cost} coins."

    # Buy successful
    users[username]["money"] -= cost
    add_potion(users, username, potion_type, 1)
    save_users(users)

    return True, f"Bought 1 {potion_type.capitalize()} Potion for {cost} coins!"
