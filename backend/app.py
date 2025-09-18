from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import os
import random

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

# Load trained model
model = joblib.load(os.path.join(os.path.dirname(__file__), "model.pkl"))

# --- Helper functions ---
def generate_repayment_plan(amount, approved):
    if not approved:
        return "Not approved. Try requesting a smaller amount."
    weekly = round(amount / 4, 2)
    return f"Repay in 4 weekly installments of ${weekly}"

def coach_message(approved):
    positive_tips = [
        "Nice work! Repaying on time could boost your credit score 💪",
        "This is a short-term safety net — let's also build long-term savings 🌱",
        "Every repayment builds confidence and future access ✅"
    ]
    denial_tips = [
        "Try requesting a smaller amount or adjusting expenses 📉",
        "Remember: budgeting tools can help free up extra cash 🧾",
        "We’re here to support — consider our financial health resources 🤝"
    ]
    return random.choice(positive_tips if approved else denial_tips)

# --- Routes ---
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory("../frontend", path)

@app.route("/predict_loan", methods=["POST"])
def predict_loan():
    data = request.json
    try:
        features = np.array([[
            float(data['income']),
            float(data['expenses']),
            float(data['amount'])
        ]])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    approved = model.predict(features)[0]
    plan = generate_repayment_plan(float(data['amount']), approved)
    tip = coach_message(approved)

    return jsonify({
        "status": "Approved" if approved else "Denied",
        "plan": plan,
        "coach": tip
    })

if __name__ == "__main__":
    app.run(debug=True)
