import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# --- Locate dataset ---
data_path = os.path.join(os.path.dirname(__file__), "data", "unexpected_expenses.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Could not find dataset at {data_path}")

print(f"✅ Loading dataset from: {data_path}")
df = pd.read_csv(data_path)

# --- Preprocessing ---
# Drop Year if present
if "Year" in df.columns:
    df = df.drop(columns=["Year"])

# Fill missing values with column means
df = df.fillna(df.mean(numeric_only=True))

# --- Define target ---
# If "All adults" >= 60 → APPROVED, else DENIED
df["target"] = df["All adults"].apply(lambda x: 1 if x >= 60 else 0)
print("Target distribution before fix:\n", df["target"].value_counts())

# Ensure at least 2 classes (synthetic fallback)
if len(df["target"].unique()) < 2:
    print("⚠️ Only one class found, adding synthetic negatives...")
    extra = df.iloc[:2].copy()
    extra["target"] = 0 if df["target"].iloc[0] == 1 else 1
    df = pd.concat([df, extra], ignore_index=True)

print("Target distribution after fix:\n", df["target"].value_counts())

# --- Features & labels ---
X = df.drop(columns=["target"])
y = df["target"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, model_path)

print("✅ Model trained and saved at", model_path)
print("Training accuracy:", model.score(X_train, y_train))
print("Test accuracy:", model.score(X_test, y_test))
