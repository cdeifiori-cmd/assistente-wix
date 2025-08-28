import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Usa la variabile d'ambiente su Render
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # Chiamata diretta al modello (senza Assistants API, solo completions)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply or "Nessuna risposta ricevuta."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
