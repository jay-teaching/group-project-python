"""
Prediction module for Telco churn model.
"""

import joblib
import pandas as pd

# IMPORTANT: Feature order must match the trained model
FEATURE_ORDER = [
    "tenure",
    "MonthlyCharges",
    "TechSupport_yes",
    "Contract_one year",
    "Contract_two year",
    "PaperlessBilling_yes",
    "InternetService_fiber optic",
    "InternetService_no",
    "PaymentMethod_credit card (automatic)",
    "PaymentMethod_electronic check",
    "PaymentMethod_mailed check",
]

BUNDLE = joblib.load("models/telco_logistic_regression.joblib")
MODEL, SCALER = BUNDLE["model"], BUNDLE["scaler"]


def make_prediction(**kwargs: float) -> float:
    """Make a churn prediction given the input features."""
    
    try:
        args = [kwargs[feature] for feature in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e.args[0]}") from e

    df = pd.DataFrame([args], columns=FEATURE_ORDER)
    scaled = SCALER.transform(df)
    prob = float(MODEL.predict_proba(scaled)[0, 1])

    print(f"Churn probability: {prob:.4f}")
    return prob
