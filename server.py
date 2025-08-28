import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# client OpenAI con la chiave da Render
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ID del tuo assistente (se vuoi usarne uno già creato)
ASSISTANT_ID = "asst_jbk2wJUFpJxXu6jDfOnF14aB"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        # nuovo endpoint Responses API
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # più veloce/economico
            messages=[
                {"role": "system", "content": "Sei un assistente utile che spiega in modo chiaro e semplice."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
