import marimo

__generated_with__ = "0.17.8"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    from pathlib import Path
    import pandas as pd
    import numpy as np

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
    from sklearn.preprocessing import StandardScaler


# ------------------------------------------------------------
# TITLE (UPDATED WITH MARIMO LIMITATION NOTE)
# ------------------------------------------------------------
@app.cell(hide_code=True)
def _():
    mo.md("""
    # Telco Churn – Feature Engineering & Model Comparison

    This notebook compares **five logistic regression models**, each using a 
    progressively richer feature set.

    ### Feature set progression:
    1. **Baseline:** tenure, MonthlyCharges, TechSupport  
    2. **+ Contract:** one-year & two-year  
    3. **+ PaperlessBilling**  
    4. **+ InternetService:** fiber optic, no internet  
    5. **+ PaymentMethod:** card, e-check, mailed check (FINAL MODEL)

    ### ⚠ Note on Marimo Plot Limitations
    Marimo does **not** auto-render Matplotlib figures (unlike Jupyter).  
    Its `mo.image()` function only accepts actual image objects (PNG bytes or PIL Images).  
    To keep this notebook simple and error‑free, Matplotlib visualizations have been removed.

    This notebook is used for **analysis only**.
    The deployed prediction model will **not** be overwritten.
    """)
    return


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------
@app.cell
def _():
    DATA_PATH = Path("input/WA_Fn-UseC_-Telco-Customer-Churn.csv")

    TEST_SIZE = 0.20
    RANDOM_STATE = 42
    SOLVER = "liblinear"
    MAX_ITER = 1000

    FEATURE_SETS = {
        "Model_1_Baseline": [
            "tenure", "MonthlyCharges", "TechSupport_yes"
        ],
        "Model_2_Contract": [
            "tenure", "MonthlyCharges", "TechSupport_yes",
            "Contract_one year", "Contract_two year"
        ],
        "Model_3_PaperlessBilling": [
            "tenure", "MonthlyCharges", "TechSupport_yes",
            "Contract_one year", "Contract_two year",
            "PaperlessBilling_yes"
        ],
        "Model_4_InternetService": [
            "tenure", "MonthlyCharges", "TechSupport_yes",
            "Contract_one year", "Contract_two year",
            "PaperlessBilling_yes",
            "InternetService_fiber optic", "InternetService_no"
        ],
        "Model_5_FinalModel": [
            "tenure", "MonthlyCharges", "TechSupport_yes",
            "Contract_one year", "Contract_two year",
            "PaperlessBilling_yes",
            "InternetService_fiber optic", "InternetService_no",
            "PaymentMethod_credit card (automatic)",
            "PaymentMethod_electronic check",
            "PaymentMethod_mailed check"
        ],
    }

    return DATA_PATH, TEST_SIZE, RANDOM_STATE, SOLVER, MAX_ITER, FEATURE_SETS


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@app.cell
def _(DATA_PATH):
    df_raw = pd.read_csv(DATA_PATH)
    return df_raw


# ------------------------------------------------------------
# PREPROCESSING
# ------------------------------------------------------------
@app.cell
def _(df_raw):
    def preprocess(df, feature_list):

        df_local = df.copy()

        if "customerID" in df_local:
            df_local = df_local.drop(columns=["customerID"])

        df_local["TotalCharges"] = pd.to_numeric(df_local["TotalCharges"], errors="coerce")
        df_local = df_local.dropna()

        for col in df_local.select_dtypes(include="object"):
            df_local[col] = df_local[col].str.lower().str.strip()

        X_full = pd.get_dummies(df_local.drop(columns=["Churn"]), drop_first=True, dtype=int)
        X_sel = X_full[feature_list]

        y = df_local["Churn"].map({"yes": 1, "no": 0}).values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_sel)

        return X_sel, X_scaled, y, scaler

    return preprocess


# ------------------------------------------------------------
# TRAIN & COMPARE MODELS
# ------------------------------------------------------------
@app.cell
def _(df_raw, preprocess, FEATURE_SETS, SOLVER, MAX_ITER, TEST_SIZE, RANDOM_STATE):

    results_list = []
    stored_models = {}
    stored_scalers = {}
    stored_feature_names = {}

    for model_name, feature_list in FEATURE_SETS.items():

        X_raw, X_scaled, y, scaler = preprocess(df_raw, feature_list)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=TEST_SIZE,
            stratify=y, random_state=RANDOM_STATE
        )

        model = LogisticRegression(
            solver=SOLVER, max_iter=MAX_ITER, random_state=RANDOM_STATE
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        results_list.append({
            "Model": model_name,
            "Num Features": len(feature_list),
            "Accuracy": accuracy_score(y_test, y_pred),
            "F1 Score": f1_score(y_test, y_pred),
            "ROC AUC": roc_auc_score(y_test, y_proba),
        })

        stored_models[model_name] = model
        stored_scalers[model_name] = scaler
        stored_feature_names[model_name] = X_raw.columns.tolist()

    df_results = pd.DataFrame(results_list)

    mo.md("## 📊 Model Comparison Table")
    mo.ui.table(df_results)

    return df_results, stored_models, stored_scalers, stored_feature_names


# ------------------------------------------------------------
# FEATURE INFLUENCE (TABLE ONLY)
# ------------------------------------------------------------
@app.cell
def _(stored_models, stored_feature_names):

    final_name = "Model_5_FinalModel"
    final_model = stored_models[final_name]
    final_features = stored_feature_names[final_name]

    coef_df = pd.DataFrame({
        "Feature": final_features,
        "Coefficient": final_model.coef_[0],
        "Absolute Impact": np.abs(final_model.coef_[0])
    }).sort_values("Absolute Impact", ascending=False)

    mo.md("## 🔍 Feature Influence – Final Model")
    mo.ui.table(coef_df)

    return


# ------------------------------------------------------------
# CONFUSION MATRIX (TABLE ONLY)
# ------------------------------------------------------------
@app.cell
def _(df_raw, preprocess, FEATURE_SETS, stored_models, TEST_SIZE, RANDOM_STATE):

    f_features = FEATURE_SETS["Model_5_FinalModel"]
    model_f = stored_models["Model_5_FinalModel"]

    X_raw_f, X_scaled_f, y_f, _ = preprocess(df_raw, f_features)

    X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
        X_scaled_f, y_f, test_size=TEST_SIZE, stratify=y_f, random_state=RANDOM_STATE
    )

    cm = confusion_matrix(y_test_f, model_f.predict(X_test_f))

    mo.md("## 📉 Confusion Matrix – Final Model")
    mo.ui.table(pd.DataFrame(cm, columns=["Pred 0", "Pred 1"], index=["True 0", "True 1"]))

    return


# ------------------------------------------------------------
# FINAL MODEL SUMMARY
# ------------------------------------------------------------
@app.cell(hide_code=True)
def _():
    mo.md("""
    ## 🏆 Final Model Selection Summary

    After evaluating five logistic regression models with progressively richer
    feature sets, the **Model_5_FinalModel** was selected for deployment.

    ### ✔ Why this model was chosen  

    **1. Strong predictive performance**  
    The final model consistently achieved:
    - **Highest ROC AUC**
    - **Highest F1 Score**
    - **Strong Accuracy**

    **2. Uses all meaningful categorical information**  
    Including contract, paperless billing, internet service, payment method,
    tech support, pricing, and tenure.

    **➡️ Conclusion:**  
    The **Model_5_FinalModel** provides the best balance of performance,
    interpretability, and simplicity for production.
    """)
    return


# ------------------------------------------------------------
# END (NO MODEL SAVING)
# ------------------------------------------------------------
@app.cell
def _():
    mo.md("""
    ## 🔒 Model Saving Disabled
    The deployed model must not be overwritten.

    This notebook is **for analysis only**.
    """)
    return


if __name__ == "__main__":
    app.run()
