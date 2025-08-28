from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    print("Messaggio ricevuto:", user_message, flush=True)  # lo vedrai nei log di Render

    return jsonify({"reply": "Ciao, funziona!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
