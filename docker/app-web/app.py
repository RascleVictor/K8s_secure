from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "App Web Sécurisée – Tout fonctionne !"})

@app.route("/healthz")
def health():
    return jsonify({"status": "OK"})

@app.route("/ready")
def ready():
    return jsonify({"status": "READY"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
