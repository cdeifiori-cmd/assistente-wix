import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Client con nuova API
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # Nuova Responses API
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # oppure gpt-4o se disponibile
            messages=[
                {"role": "system", "content": "Sei un assistente che spiega l'Analisi Transazionale."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
