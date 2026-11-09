from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return (
        "<h1>Hello from Docker and Kubernetes!</h1>"
        "<p>Assignment 1 - Containerized Flask App</p>"
        f"<p>Served by: <b>{socket.gethostname()}</b></p>"
    )

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)