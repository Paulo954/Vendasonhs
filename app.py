from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

DADOS_FILE = "dados.json"

# Criar arquivo se não existir
def load_data():
    if not os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, "w") as f:
            json.dump({"vendas": [], "lucros": []}, f)

    with open(DADOS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"vendas": [], "lucros": []}

def save_data(data):
    with open(DADOS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        senha = request.form.get("senha")

        if user == "julia" and senha == "07022025":
            return redirect(url_for("painel"))
        else:
            return render_template("login.html", erro="Login inválido")

    return render_template("login.html")

# PAINEL
@app.route("/painel")
def painel():
    data = load_data()
    return render_template("painel.html", vendas=data["vendas"], lucros=data["lucros"])

# ADD VENDA
@app.route("/add_venda", methods=["POST"])
def add_venda():
    data = load_data()
    valor = request.json.get("valor")

    if valor:
        data["vendas"].append(float(valor))
        save_data(data)

    return jsonify(data)

# ADD LUCRO
@app.route("/add_lucro", methods=["POST"])
def add_lucro():
    data = load_data()
    valor = request.json.get("valor")

    if valor:
        data["lucros"].append(float(valor))
        save_data(data)

    return jsonify(data)

# REMOVER VENDA
@app.route("/remove_venda", methods=["POST"])
def remove_venda():
    data = load_data()
    index = request.json.get("index")

    if index is not None and 0 <= index < len(data["vendas"]):
        data["vendas"].pop(index)
        save_data(data)

    return jsonify(data)

# REMOVER LUCRO
@app.route("/remove_lucro", methods=["POST"])
def remove_lucro():
    data = load_data()
    index = request.json.get("index")

    if index is not None and 0 <= index < len(data["lucros"]):
        data["lucros"].pop(index)
        save_data(data)

    return jsonify(data)

# RESUMO
@app.route("/resumo")
def resumo():
    data = load_data()
    return jsonify(
        total_vendas=sum(data["vendas"]),
        total_lucro=sum(data["lucros"])
    )

# VER JSON
@app.route("/ver_dados")
def ver_dados():
    data = load_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)