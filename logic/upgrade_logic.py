# logic/upgrade_logic.py
import os
from logic.inventory_logic import load_users, save_users

# Costs and caps
ATTACK_BASE = 8
ATTACK_INC  = 8
ATTACK_CAP  = 5  # +3 ATK each time

HEALTH_BASE = 10
HEALTH_INC  = 10
HEALTH_CAP  = 3  # +8 HP each time

LUCK_BASE   = 15
LUCK_INC    = 15
LUCK_CAP    = 3  # total levels (stats.luck goes 1 -> 2 -> 3)

def _find_pokemon_ref(users, username, name):
    """Return a direct reference to the first Pokémon with this name in THIS users dict."""
    username = username.lower()
    for p in users[username]["pokemon"]:
        if p.get("name", "").lower() == (name or "").lower():
            return p
    return None

def _ensure_upgrade_fields(p):
    """Make sure upgrade counters exist on older Pokémon."""
    if "attack_upgrades" not in p: p["attack_upgrades"] = 0
    if "health_upgrades" not in p: p["health_upgrades"] = 0

def _attack_cost_for(p):
    return ATTACK_BASE + ATTACK_INC * p.get("attack_upgrades", 0)

def _health_cost_for(p):
    return HEALTH_BASE + HEALTH_INC * p.get("health_upgrades", 0)

def _luck_cost_for(users, username):
    # luck starts at 1; upgrades done = (luck - 1)
    level = users[username]["stats"]["luck"]
    upgrades_done = max(0, level - 1)
    return LUCK_BASE + LUCK_INC * upgrades_done

def upgrade_attack(username, pokemon_name):
    users = load_users()
    username = username.lower()

    # must own at least one Pokémon
    if not users[username]["pokemon"]:
        return False, "You have no Pokémon yet. Open a chest first."

    if not pokemon_name:
        return False, "Select a Pokémon to upgrade."

    p = _find_pokemon_ref(users, username, pokemon_name)
    if p is None:
        return False, "Pokémon not found."

    _ensure_upgrade_fields(p)

    if p["attack_upgrades"] >= ATTACK_CAP:
        return False, "Attack is already maxed for this Pokémon."

    cost = _attack_cost_for(p)
    if users[username]["xp"] < cost:
        return False, f"Not enough XP. Attack costs {cost} XP."

    # apply
    users[username]["xp"] -= cost
    p["attack"] += 3
    p["attack_upgrades"] += 1

    save_users(users)
    return True, f"{p['name']} gained +3 Attack (cost {cost} XP)."

def upgrade_health(username, pokemon_name):
    users = load_users()
    username = username.lower()

    if not users[username]["pokemon"]:
        return False, "You have no Pokémon yet. Open a chest first."

    if not pokemon_name:
        return False, "Select a Pokémon to upgrade."

    p = _find_pokemon_ref(users, username, pokemon_name)
    if p is None:
        return False, "Pokémon not found."

    _ensure_upgrade_fields(p)

    if p["health_upgrades"] >= HEALTH_CAP:
        return False, "Health is already maxed for this Pokémon."

    cost = _health_cost_for(p)
    if users[username]["xp"] < cost:
        return False, f"Not enough XP. Health costs {cost} XP."

    users[username]["xp"] -= cost
    p["max_hp"] += 8
    p["hp"] = p["max_hp"]  # heal to full
    p["health_upgrades"] += 1

    save_users(users)
    return True, f"{p['name']} gained +8 HP (cost {cost} XP)."

def upgrade_luck(username):
    users = load_users()
    username = username.lower()

    # luck levels are 1..3
    if users[username]["stats"]["luck"] >= LUCK_CAP:
        return False, "Luck is already maxed."

    cost = _luck_cost_for(users, username)
    if users[username]["xp"] < cost:
        return False, f"Not enough XP. Luck costs {cost} XP."

    users[username]["xp"] -= cost
    users[username]["stats"]["luck"] += 1

    save_users(users)
    return True, f"Luck increased by +1 (cost {cost} XP)."
