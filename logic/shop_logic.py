import json
import os
from logic.inventory_logic import load_users, save_users, add_key, add_potion

DATA_PATH = os.path.join("data", "users.json")


# -------------------- Shop Prices --------------------

PRICES = {
    "keys": {
        "wooden": 10,
        "iron": 25,
        "gold": 50,
        "mythic": 100,
        "ultimate": 200
    },

    "chests": {
        "wooden": 15,
        "iron": 40,
        "gold": 80,
        "mythic": 150,
        "ultimate": 300
    },

    "potions": {
        "heal": 20,
        "xp": 30
    }
}


# -------------------- Buy Key --------------------

def buy_key(username, key_type):
    username = username.lower()
    users = load_users()

    if key_type not in PRICES["keys"]:
        return False, "Invalid key type."

    cost = PRICES["keys"][key_type]

    if users[username]["money"] < cost:
        return False, "Not enough money."

    users[username]["money"] -= cost
    add_key(username, key_type)
    save_users(users)

    return True, f"Purchased {key_type} key for {cost} coins."


# -------------------- Buy Chest --------------------

def buy_chest(username, chest_type):
    username = username.lower()
    users = load_users()

    if chest_type not in PRICES["chests"]:
        return False, "Invalid chest type."

    cost = PRICES["chests"][chest_type]

    if users[username]["money"] < cost:
        return False, "Not enough money."

    users[username]["money"] -= cost
    save_users(users)

    return True, f"Purchased a {chest_type} chest for {cost} coins."


# -------------------- Buy Potion --------------------

def buy_potion(username, potion_type):
    username = username.lower()
    users = load_users()

    if potion_type not in PRICES["potions"]:
        return False, "Invalid potion type."

    cost = PRICES["potions"][potion_type]

    if users[username]["money"] < cost:
        return False, "Not enough money."

    users[username]["money"] -= cost
    add_potion(username, potion_type)
    save_users(users)

    return True, f"Purchased {potion_type} potion for {cos_
