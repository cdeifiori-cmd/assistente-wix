import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # abilita richieste cross-origin (da Wix)

# Client OpenAI con variabile d'ambiente
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ASSISTANT_ID = "asst_jbk2wJUFpJxXu6jDfOnF14aB"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Messaggio mancante"}), 400

        # 1. Crea un thread
        thread = client.beta.threads.create()

        # 2. Aggiungi messaggio dell’utente
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # 3. Avvia il run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4. Recupera la risposta
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        reply = None
        for msg in reversed(messages.data):
            if msg.role == "assistant" and msg.content and msg.content[0].type == "text":
                reply = msg.content[0].text.value
                break

        return jsonify({"reply": reply or "Nessuna risposta ricevuta."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
