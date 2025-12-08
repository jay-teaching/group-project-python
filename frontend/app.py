import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "https://<YOUR-FUNCTION-APP>.azurewebsites.net/api/predict"

st.title("📊 Telco Customer Churn Prediction")

tenure = st.slider("Customer Tenure (months)", 0, 72, 12)
monthly = st.slider("Monthly Charges ($)", 0.0, 150.0, 70.0)
techsupport = st.selectbox("Tech Support Included?", ["No", "Yes"])
paperless = st.selectbox("Paperless Billing?", ["No", "Yes"])
contract_months = st.slider("Contract Length (months)", 1, 36, 12)

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"],
)

payment_method = st.selectbox(
    "Payment Method",
    [
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)"  # baseline (all zeros)
    ]
)

if st.button("Predict Churn Probability"):
    params = {
        "tenure": tenure,
        "monthly": monthly,
        "techsupport": 1 if techsupport == "Yes" else 0,
        "paperless": 1 if paperless == "Yes" else 0,
        "contract_months": contract_months,
        "internet_service": internet_service,
        "payment_method": payment_method,
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        prob = float(response.text)
        st.success(f"Churn probability: {prob:.2%}")

        fig, ax = plt.subplots(figsize=(6, 1.5))
        ax.barh(["Churn Probability"], [prob])
        ax.set_xlim(0, 1)
        st.pyplot(fig)

    else:
        st.error(response.text)
