import json
import os
import random
from logic.inventory_logic import load_users, save_users, remove_key, add_potion

POKEMON_POOL_PATH = os.path.join("data", "pokemon_pool.json")
CHEST_LOOT_PATH = os.path.join("data", "chest_loot.json")


# -------------------- Loaders --------------------

def load_pokemon_pool():
    with open(POKEMON_POOL_PATH, "r") as f:
        return json.load(f)


def load_chest_loot():
    with open(CHEST_LOOT_PATH, "r") as f:
        return json.load(f)


# -------------------- Open Chest --------------------

def open_chest(username, chest_type):
    username = username.lower()

    chest_loot = load_chest_loot()
    if chest_type not in chest_loot:
        return False, "Invalid chest type.", None

    # 1) Consume the key (this saves internally)
    if not remove_key(username, chest_type, 1):
        return False, f"You don't have a {chest_type} key!", None

    # 2) Build a working rarity table and apply Luck
    rarity_table = chest_loot[chest_type].copy()

    users_for_luck = load_users()  # fresh read after key change
    luck = users_for_luck[username]["stats"].get("luck", 0)

    # Your rule: per Luck level, -4% from first, +2% to each of the last two
    rarities_in_order = list(rarity_table.keys())
    if luck > 0 and len(rarities_in_order) >= 3:
        first = rarities_in_order[0]
        last1 = rarities_in_order[-1]
        last2 = rarities_in_order[-2]

        rarity_table[first] = max(0, rarity_table[first] - 4 * luck)
        rarity_table[last1] = rarity_table[last1] + 2 * luck
        rarity_table[last2] = rarity_table[last2] + 2 * luck

    # 3) Choose rarity using the (possibly shifted) table
    rarity = choose_rarity(rarity_table)

    # 4) Pick Pokémon and create its data
    pool = load_pokemon_pool()
    if rarity not in pool or not pool[rarity]:
        # Fallback if pool is missing something
        for r in ["common", "rare", "epic", "mythic", "legendary"]:
            if r in pool and pool[r]:
                rarity = r
                break

    pdef = random.choice(pool[rarity])
    new_pokemon = format_pokemon_data(pdef["name"], pdef["type"], rarity)

    # 5) Append Pokémon and save (save once here)
    users = load_users()  # fresh copy after key removal
    users[username]["pokemon"].append(new_pokemon)
    save_users(users)

    # 6) Give a potion (this loads+saves internally)
    potion = random.choice(["heal", "xp"])
    add_potion(username, potion, 1)

    # 7) Return reward info
    reward = {
        "pokemon": new_pokemon,
        "potion": potion
    }
    return True, f"You opened a {chest_type} chest!", reward


# -------------------- Rarity Choice --------------------

def choose_rarity(table):
    """Pick a rarity from a dict like {'common': 80, 'rare': 15, 'epic': 5}."""
    total = sum(max(0, v) for v in table.values())
    if total <= 0:
        # Degenerate case: pick the last defined rarity
        return list(table.keys())[-1]

    roll = random.randint(1, total)
    cumulative = 0
    for rarity, chance in table.items():
        val = max(0, chance)
        cumulative += val
        if roll <= cumulative:
            return rarity

    # Fallback safety
    return list(table.keys())[-1]


# -------------------- Pokémon Factory --------------------

def format_pokemon_data(name, type_, rarity):
    base_stats = {
        "common":    {"hp": 40,  "attack": 8,  "defense": 6},
        "rare":      {"hp": 60,  "attack": 12, "defense": 8},
        "epic":      {"hp": 80,  "attack": 16, "defense": 12},
        "mythic":    {"hp": 100, "attack": 20, "defense": 15},
        "legendary": {"hp": 120, "attack": 25, "defense": 18}
    }
    stats = base_stats.get(rarity, base_stats["common"])

    return {
        "name": name,
        "type": type_,
        "rarity": rarity,
        "level": 1,

        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "moves": [],

        # per-Pokémon upgrade tracking (used by upgrade_logic)
        "attack_upgrades": 0,
        "health_upgrades": 0
    }
