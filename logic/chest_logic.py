import json
import os
import random
from logic.inventory_logic import load_users, save_users, remove_key, add_potion

USERS_PATH = os.path.join("data", "users.json")
POKEMON_POOL_PATH = os.path.join("data", "pokemon_pool.json")
CHEST_LOOT_PATH = os.path.join("data", "chest_loot.json")


# -------------------- Load Data --------------------

def load_pokemon_pool():
    with open(POKEMON_POOL_PATH, "r") as f:
        return json.load(f)


def load_chest_loot():
    with open(CHEST_LOOT_PATH, "r") as f:
        return json.load(f)


# -------------------- Chest Opening --------------------

def open_chest(username, chest_type):
    """
    Main function to open a chest.
    Returns: (success, message, reward_data)
    reward_data includes the Pokémon + potion gained.
    """
    username = username.lower()

    users = load_users()
    pokemon_pool = load_pokemon_pool()
    chest_loot = load_chest_loot()

    # 1. Check chest type exists
    if chest_type not in chest_loot:
        return False, "Invalid chest type.", None

    # 2. Check the user has the correct key
    key_name = chest_type  # keys have same name as chests
    if not remove_key(username, key_name):
        return False, f"You don't have a {key_name} key!", None

    # 3. Choose rarity based on percentages
    rarity = choose_rarity(chest_loot[chest_type])

    # 4. Pick Pokémon from that rarity pool
    pokemon = random.choice(pokemon_pool[rarity])

    # 5. Generate Pokémon stats
    new_pokemon = format_pokemon_data(pokemon["name"], pokemon["type"], rarity)

    # 6. Add Pokémon to user
    users[username]["pokemon"].append(new_pokemon)

    # 7. Give 1 random potion (heal or xp)
    potion_reward = random.choice(["heal", "xp"])
    add_potion(username, potion_reward, 1)

    # Save changes
    save_users(users)

    reward_data = {
        "pokemon": new_pokemon,
        "potion": potion_reward
    }

    return True, f"You opened a {chest_type} chest!", reward_data


# -------------------- Choose Rarity --------------------

def choose_rarity(rarity_table):
    """
    rarity_table example:
    { "common": 60, "rare": 30, "epic": 10, ... }
    """
    roll = random.randint(1, 100)
    cumulative = 0

    for rarity, chance in rarity_table.items():
        cumulative += chance
        if roll <= cumulative:
            return rarity

    return "common"  # fallback safety


# -------------------- Format Pokémon Data --------------------

def format_pokemon_data(name, type_, rarity):
    """
    Create a Pokémon dictionary with starter stats.
    You can adjust these values anytime.
    """
    base_stats = {
        "common":    {"hp": 40,  "attack": 8,  "defense": 6,  "luck": 1},
        "rare":      {"hp": 60,  "attack": 12, "defense": 8,  "luck": 2},
        "epic":      {"hp": 80,  "attack": 16, "defense": 12, "luck": 3},
        "mythic":    {"hp": 100, "attack": 20, "defense": 15, "luck": 4},
        "legendary": {"hp": 120, "attack": 25, "defense": 18, "luck": 5}
    }

    stats = base_stats[rarity]

    return {
        "name": name,
        "type": type_,
        "rarity": rarity,
        "level": 1,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "luck": stats["luck"],
        "moves": []   # For now empty — you can add custom moves later
    }
