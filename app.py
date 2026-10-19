import os
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "cofrinho123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route("/", methods=["GET"])
def home():
    return "Cofrinho online! 🐷", 200

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro de verificação", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Dados: {data}")
    if data and "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")
                if messages:
                    for msg in messages:
                        from_number = msg["from"]
                        text = msg.get("text", {}).get("body", "").lower()
                        print(f"Msg de {from_number}: {text}")
                        if "oi" in text or "cofrinho" in text:
                            resposta = "Olá! Sou o Cofrinho 🐷💰 Me diga quanto gastou, ex: Gastei 20 com lanche"
                        else:
                            resposta = f"Recebi: {text}. Me diga seus gastos!"
                        enviar_mensagem(from_number, resposta)
    return "OK", 200

def enviar_mensagem(to, texto):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": texto}
    }
    print(f"Enviando para {to}: {texto}")
    r = requests.post(url, headers=headers, json=payload)
    print(f"Resposta API: {r.status_code} - {r.text}")
    return r

@app.route("/test", methods=["GET"])
def test_envio():
    to = request.args.get("to", "5524974028012")
    r = enviar_mensagem(to, "Teste do Cofrinho 🐷 funcionou!")
    return f"Status: {r.status_code}<br>Resposta: {r.text}", r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
