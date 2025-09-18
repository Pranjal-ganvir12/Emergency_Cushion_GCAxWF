from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import os
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 👇 Serve frontend
@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

# 👇 Your ML API
@app.route("/predict_loan", methods=["POST"])
@app.route("/predict_loan", methods=["POST"])
def predict_loan():
    data = request.get_json()
    income = float(data.get("income", 0))
    expenses = float(data.get("expenses", 0))
    amount = float(data.get("amount", 0))

    # Example approval logic
    if income - expenses > amount * 0.3:
        return jsonify({
            "status": "APPROVED",
            "repayment": "4 easy installments over 2 months",  # ✅ return plan
            "coach": "Great work balancing!"
        })
    else:
        return jsonify({
            "status": "DENIED",
            "repayment": "Consider requesting a smaller amount or adjusting expenses.",
            "coach": "Try lowering the requested loan or increasing savings."
        })

if __name__ == "__main__":
    app.run(debug=True)
