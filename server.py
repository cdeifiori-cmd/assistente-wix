import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# prende la chiave da Render
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ID del tuo assistente
ASSISTANT_ID = "asst_jbk2wJUFpJxXu6jDfOnF14aB"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # 1. Crea un thread
        thread = client.beta.threads.create()

        # 2. Aggiungi messaggio utente
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # 3. Avvia il run con l’assistente
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4. Recupera la risposta
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        reply = None
        for msg in reversed(messages.data):
            if msg.role == "assistant" and msg.content:
                reply = msg.content[0].text.value
                break

        return jsonify({"reply": reply or "Nessuna risposta ricevuta."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
