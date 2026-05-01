from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "qualquer_coisa_forte_123456"

USER = "admin"
PASS = "12121980"

# ======================
# JSON
# ======================

def load_estoque():
    try:
        with open("estoque.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_estoque(data):
    with open("estoque.json", "w") as f:
        json.dump(data, f, indent=4)

def load_guilds():
    try:
        with open("guilds.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_guilds(data):
    with open("guilds.json", "w") as f:
        json.dump(data, f, indent=4)

# ======================
# SITE LOGIN
# ======================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == USER and request.form["senha"] == PASS:
            session["logado"] = True
            return redirect("/painel")
        else:
            return "❌ Login inválido"
    return render_template("login.html")

@app.route("/painel")
def painel():
    if not session.get("logado"):
        return redirect("/")

    return render_template(
        "index.html",
        estoque=load_estoque(),
        guilds=load_guilds()
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================
# ROTAS DO SITE (FIX DO NOT FOUND)
# ======================

@app.route("/add", methods=["POST"])
def add():
    estoque = load_estoque()

    gid = request.form["guild"]
    item = request.form["item"]
    qtd = int(request.form["qtd"])

    if gid not in estoque:
        estoque[gid] = {}

    estoque[gid][item] = estoque[gid].get(item, 0) + qtd

    save_estoque(estoque)
    return redirect("/painel")


@app.route("/remover", methods=["POST"])
def remover():
    estoque = load_estoque()

    gid = request.form["guild"]
    item = request.form["item"]
    qtd = int(request.form["qtd"])

    if gid in estoque and item in estoque[gid]:
        estoque[gid][item] -= qtd

        if estoque[gid][item] <= 0:
            del estoque[gid][item]

    save_estoque(estoque)
    return redirect("/painel")

# ======================
# API BOT
# ======================

@app.route("/api/estoque", methods=["GET"])
def api_get_estoque():
    return jsonify(load_estoque())

@app.route("/api/estoque/update", methods=["POST"])
def api_update_estoque():
    data = request.json
    save_estoque(data)
    return jsonify({"status": "ok"})

@app.route("/api/guilds", methods=["GET"])
def api_get_guilds():
    return jsonify(load_guilds())

@app.route("/api/guilds/update", methods=["POST"])
def api_update_guilds():
    data = request.json
    save_guilds(data)
    return jsonify({"status": "ok"})

# ======================
# START
# ======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
