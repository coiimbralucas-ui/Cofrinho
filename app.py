from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "cofrinho123"
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN", os.environ.get("ACCESS_TOKEN", ""))
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
    data = request.get_json()
    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            msg = entry["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"].lower()

            # Lógica simples do Cofrinho
            if "saldo" in text:
                resposta = "Seu cofrinho está com R$ 0,00 por enquanto! Me diga 'guardei 10' para começar."
            elif "guardei" in text or "gastei" in text:
                resposta = f"Anotado: {text} ✅"
            else:
                resposta = "Oi! Sou seu Cofrinho 🐷\nMe diga:\n- guardei 10\n- gastei 5\n- saldo"

            # Envia resposta
            url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": resposta}
            }
            requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print(f"Erro: {e}")
    
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Cofrinho rodando!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
