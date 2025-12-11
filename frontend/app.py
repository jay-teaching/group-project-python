import matplotlib.pyplot as plt
import requests
import streamlit as st
from matplotlib.ticker import PercentFormatter

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
# MODEL INFO PANEL
# -----------------------
with st.expander("ℹ️ About this Model"):
    st.markdown("""
    **Dataset**: IBM Telco Customer Churn (7,043 customers)
    
    **Model**: Logistic Regression trained on customer demographics, services, and billing data.
    
    **Performance**: 
    - Accuracy: ~80%
    - Identifies high-risk customers
    
    **Features Used** for Prediction:
    - Customer tenure in months
    - Monthly charges
    - Tech support subscription
    - Paperless billing preference
    - Contract length
    - Internet service type
    - Payment method
    """)

# -----------------------
# INPUT UI
# -----------------------
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider(
        "Customer Tenure (months)",
        0, 72, 12,
        help="How long the customer has been with the company. Longer tenure typically indicates lower churn risk."
    )
    techsupport = st.selectbox(
        "Tech Support Included?",
        ["No", "Yes"],
        help="Customers with tech support tend to have lower churn rates."
    )
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
        ],
        help="Payment method can indicate customer engagement. Electronic check users often have higher churn."
    )

with col2:
    monthly = st.slider(
        "Monthly Charges ($)",
        0.0, 150.0, 70.0,
        help="Higher monthly charges can correlate with increased churn risk if value isn't perceived."
    )
    paperless = st.selectbox(
        "Paperless Billing?",
        ["No", "Yes"],
        help="Indicates customer's digital engagement preference."
    )
    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"],
        help="Type of internet service. Fiber optic customers may have different churn patterns than DSL."
    )

contract_months = st.slider(
    "Contract Length (months)",
    1, 36, 12,
    help="Contract commitment. Month-to-month (1) has highest churn, 2-year (24) has lowest."
)

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
                response = requests.post(API_URL, json=params, timeout=10)

                if response.status_code == 200:
                    prob = response.json()["churn_probability"]

                    # added: risk interpretation based on probability threshold
                    if prob > 0.2:
                        st.warning(f"🚨 High churn risk: {prob:.2%}")
                    else:
                        st.success(f"✅ Low churn risk: {prob:.2%}")

                    st.markdown(
                        f"""
                        <div class='result-card'>
                            <div class='result-prob'>{prob:.2%}</div>
                            <p>Predicted likelihood of churn, a figure above 20% is considered risky</p>
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
                    ax.xaxis.set_major_formatter(PercentFormatter(1.0))
                    st.pyplot(fig)

                elif response.status_code == 400:
                    st.error(f"❌ Invalid input: {response.text}")
                elif response.status_code == 500:
                    st.error("🔧 Server error - please try again later")
                else:
                    st.error(f"⚠️ Unexpected error (status {response.status_code}): {response.text}")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out - the server took too long to respond")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection failed - unable to reach the prediction service")
            except requests.exceptions.RequestException as e:
                st.error(f"🌐 Network error: {e}")
            except ValueError as e:
                st.error(f"📊 Invalid response format: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
