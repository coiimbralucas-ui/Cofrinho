from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "cofrinho123")
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN", os.environ.get("ACCESS_TOKEN", ""))
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")
# Coloque seu token depois aqui
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "SEU_TOKEN_AQUI")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "erro token", 403

@app.route("/webhook", methods=["POST"])
def incoming():
    data = request.json
    print(data)
    # Aqui depois a gente coloca a lógica do cofrinho
    return "ok", 200

@app.route("/")
def home():
    return "Cofrinho 24h ON - Webhook ativo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
