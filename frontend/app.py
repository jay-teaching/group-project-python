import streamlit as st
import requests
import matplotlib.pyplot as plt

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="Telco Churn Prediction",
    page_icon="📊",
    layout="centered",
)

API_URL = "https://telco-backend.politeriver-aee86836.norwayeast.azurecontainerapps.io/predict"

# -----------------------
# CUSTOM CSS
# -----------------------
st.markdown(
    """
    <style>

    /* Main page width */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    /* Title styling */
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #2B2D42 !important;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #6A6A6A;
        margin-bottom: 2rem;
    }

    /* Increase slider label size */
    .stSlider label, .stSelectbox label {
        font-weight: 600 !important;
        color: #333 !important;
    }

    /* Card style for prediction */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 1.5rem;
    }

    .result-prob {
        font-size: 2.2rem;
        font-weight: 700;
        color: #D90429;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# TITLE
# -----------------------
st.markdown("<h1>📊 Telco Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Adjust customer attributes to estimate the likelihood of churn.</p>",
    unsafe_allow_html=True,
)

# -----------------------
# INPUT UI
# -----------------------
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Customer Tenure (months)", 0, 72, 12)
    techsupport = st.selectbox("Tech Support Included?", ["No", "Yes"])
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
        ]
    )

with col2:
    monthly = st.slider("Monthly Charges ($)", 0.0, 150.0, 70.0)
    paperless = st.selectbox("Paperless Billing?", ["No", "Yes"])
    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"],
    )

contract_months = st.slider("Contract Length (months)", 1, 36, 12)

# -----------------------
# BUTTON + API CALL
# -----------------------
if st.button("🔮 Predict Churn Probability"):
    # added: input validation to prevent empty predictions
    if tenure == 0 or monthly == 0.0:
        st.warning("⚠️ Tenure and monthly charges must be > 0")
    else:
        # added: loading spinner for better ux
        with st.spinner("⏳ Predicting..."):
            params = {
                "tenure": tenure,
                "monthly": monthly,
                "techsupport": 1 if techsupport == "Yes" else 0,
                "paperless": 1 if paperless == "Yes" else 0,
                "contract_months": contract_months,
                "internet_service": internet_service,
                "payment_method": payment_method,
            }

            try:
                response = requests.post(API_URL, json=params)

                if response.status_code == 200:
                    prob = response.json()["churn_probability"]

                    # added: risk interpretation based on probability threshold
                    if prob > 0.5:
                        st.warning(f"🚨 High churn risk: {prob:.2%}")
                    else:
                        st.success(f"✅ Low churn risk: {prob:.2%}")

                    st.markdown(
                        f"""
                        <div class='result-card'>
                            <div class='result-prob'>{prob:.2%}</div>
                            <p>Predicted likelihood of churn</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # gauge-style bar chart
                    fig, ax = plt.subplots(figsize=(6, 1.2))
                    ax.barh([""], [prob], color="#D90429")
                    ax.set_xlim(0, 1)
                    ax.set_yticks([])
                    ax.set_xlabel("Churn Probability")
                    st.pyplot(fig)

                else:
                    st.error(f"API Error: {response.text}")

            except Exception as e:
                st.error(f"Connection failed: {e}")
