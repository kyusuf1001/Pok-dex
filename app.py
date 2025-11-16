from flask import Flask, render_template, request, redirect, url_for
import os
import json

# Import logic files
from logic.inventory_logic import load_users, save_users, get_inventory
from logic.pokemon_logic import get_pokemon_list, get_pokemon, set_active_pokemon, get_active_pokemon
from logic.chest_logic import open_chest
from logic.shop_logic import buy_key, buy_chest, buy_potion
from logic.battle_logic import apply_damage, heal_active, reward_for_win

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()

        users = load_users()
        if username in users:
            return redirect(url_for("dashboard", username=username))
        else:
            return render_template("login.html", error="User not found.")

    return render_template("login.html")

@app.route("/<username>/dashboard")
def dashboard(username):
    username = username.lower()
    users = load_users()

    data = users[username]
    active = get_active_pokemon(username)

    return render_template("dashboard.html", username=username, data=data, active=active)

@app.route("/<username>/inventory")
def inventory(username):
    username = username.lower()
    inv = get_inventory(username)

    users = load_users()
    money = users[username]["money"]
    xp = users[username]["xp"]

    return render_template("inventory.html", username=username, inv=inv, money=money, xp=xp)

@app.route("/<username>/shop", methods=["GET", "POST"])
def shop(username):
    username = username.lower()
    message = None

    if request.method == "POST":
        item = request.form.get("item")
        type_ = request.form.get("type")

        if item == "key":
            success, message = buy_key(username, type_)
        elif item == "chest":
            success, message = buy_chest(username, type_)
        elif item == "potion":
            success, message = buy_potion(username, type_)

    users = load_users()
    money = users[username]["money"]

    return render_template("shop.html", username=username, money=money, message=message)

@app.route("/<username>/chests", methods=["GET", "POST"])
def chests(username):
    username = username.lower()
    message = None
    reward = None

    if request.method == "POST":
        chest_type = request.form.get("chest_type")
        success, message, reward = open_chest(username, chest_type)

    users = load_users()
    inv = users[username]["inventory"]["keys"]

    return render_template("chests.html",
                           username=username,
                           keys=inv,
                           message=message,
                           reward=reward)

@app.route("/<username>/pokemon")
def pokemon_list_page(username):
    username = username.lower()
    pokes = get_pokemon_list(username)

    return render_template("pokemon_list.html", username=username, pokemon=pokes)

@app.route("/<username>/pokemon/<pname>")
def pokemon_detail(username, pname):
    username = username.lower()
    p = get_pokemon(username, pname)

    return render_template("pokemon_detail.html", username=username, p=p)

@app.route("/<username>/set_active/<pname>")
def set_active(username, pname):
    username = username.lower()
    success, msg = set_active_pokemon(username, pname)
    return redirect(url_for("dashboard", username=username))

@app.route("/<username>/battle", methods=["GET", "POST"])
def battle(username):
    username = username.lower()
    message = None

    if request.method == "POST":
        action = request.form.get("action")

        # Damage taken
        if action == "damage":
            amt = int(request.form.get("amount"))
            success, message = apply_damage(username, amt)

        # Healing
        elif action == "heal":
            amt = int(request.form.get("amount"))
            success, message = heal_active(username, amt)

        # Win reward
        elif action == "win":
            rarity = request.form.get("rarity")
            success, message = reward_for_win(username, rarity)

    active = get_active_pokemon(username)

    return render_template("battle_helper.html", username=username, active=active, message=message)

@app.route("/<username>/upgrades", methods=["GET", "POST"])
def upgrades(username):
    username = username.lower()
    users = load_users()

    message = None

    if request.method == "POST":
        stat = request.form.get("stat")

        # cost increases with each stat level
        cost = users[username]["stats"][stat] * 10

        if users[username]["xp"] < cost:
            message = "Not enough XP!"
        else:
            users[username]["xp"] -= cost
            users[username]["stats"][stat] += 1
            save_users(users)
            message = f"{stat.capitalize()} upgraded!"

    return render_template("upgrade_stats.html", username=username, stats=users[username]["stats"], xp=users[username]["xp"], message=message)

if __name__ == "__main__":
    app.run(debug=True)
