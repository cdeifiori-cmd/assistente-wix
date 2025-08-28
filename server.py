import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Client OpenAI con API Key (letta da Render → Environment Variables)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Qui inserisci l’ID del tuo Assistente (lo trovi su platform.openai.com → Assistants)
ASSISTANT_ID = "asst_jbk2wJUFpJxXu6jDfOnF14aB"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # 1. Crea thread
        thread = client.beta.threads.create()

        # 2. Aggiungi messaggio utente
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # 3. Avvia il run con il tuo Assistente
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4. Recupera ultima risposta dell'assistente
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        reply = None
        for msg in reversed(messages.data):
            if msg.role == "assistant" and msg.content and msg.content[0].type == "text":
                reply = msg.content[0].text.value
                break

        return jsonify({"reply": reply or "⚠️ Nessuna risposta ricevuta da OpenAI."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
