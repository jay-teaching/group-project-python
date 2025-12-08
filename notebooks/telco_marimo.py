import marimo

__generated_with__ = "0.17.8"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path
    import joblib
    import marimo as mo
    import pandas as pd

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        confusion_matrix,
        f1_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler


# TITLE
@app.cell(hide_code=True)
def _():
    mo.md("""
    # Telco churn – interactive logistic regression

    Use the feature selector below to experiment with different model inputs.
    The notebook retrains automatically whenever you change features.
    """)
    return


# CONSTANTS
@app.cell
def _():
    DATA_PATH = Path("input/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    MODEL_SAVE_PATH = Path("models/telco_logistic_regression.joblib")

    SAVE_MODEL = False  # Set to True only when saving final model
    TEST_SIZE = 0.20
    C_VALUE = 1.0
    MAX_ITER = 1000
    SOLVER = "liblinear"

    return (
        C_VALUE,
        DATA_PATH,
        MAX_ITER,
        MODEL_SAVE_PATH,
        SAVE_MODEL,
        SOLVER,
        TEST_SIZE,
    )


# LOAD RAW DATA
@app.cell
def _(DATA_PATH):
    telco_df = pd.read_csv(DATA_PATH)

    mo.md("### Raw Telco Dataset")
    mo.ui.table(telco_df.head())

    return telco_df,

# INTERACTIVE FEATURE SELECTION
@app.cell
def _():
    mo.md("### Select model features")

    all_features = [
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

    SELECTED_FEATURES = mo.ui.multiselect(
        label="Choose model features:",
        options=all_features,
        value=[
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
        ],
    )

    SELECTED_FEATURES
    return SELECTED_FEATURES,



# PREPROCESSING
@app.cell
def _(SELECTED_FEATURES, telco_df):
    def preprocess_telco(df: pd.DataFrame, selected):
        cleaned = df.copy()

        # Remove ID column
        if "customerID" in cleaned.columns:
            cleaned = cleaned.drop(columns=["customerID"])

        # Fix TotalCharges
        cleaned["TotalCharges"] = pd.to_numeric(cleaned["TotalCharges"], errors="coerce")
        cleaned = cleaned.dropna()

        # Normalize text columns
        for c in cleaned.select_dtypes(include="object"):
            cleaned[c] = cleaned[c].str.lower().str.strip()

        # One-hot encode
        X = pd.get_dummies(cleaned.drop(columns=["Churn"]), drop_first=True, dtype=int)

        print("Available features:", X.columns.tolist())
        print("Selected:", list(selected.value))

        # Select chosen features
        X = X[list(selected.value)]
        y = cleaned["Churn"].map({"yes": 1, "no": 0}).to_numpy()

        # Scale
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return cleaned, X_scaled, y, scaler, X.columns.tolist()

    cleaned_df, X_scaled, y, scaler, feature_names = preprocess_telco(
        telco_df, SELECTED_FEATURES
    )

    mo.md("### Cleaned Dataset")
    mo.ui.table(cleaned_df.head())

    return X_scaled, scaler, y, feature_names


# TRAINING
@app.cell
def _(C_VALUE, MAX_ITER, SOLVER, TEST_SIZE, X_scaled, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=42,
    )

    model = LogisticRegression(
        solver=SOLVER, C=C_VALUE, max_iter=MAX_ITER, random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion": confusion_matrix(y_test, y_pred),
        "report": classification_report(y_test, y_pred),
    }

    mo.md(f"""
    ### Model Metrics  
    **Accuracy:** {metrics["accuracy"]:.4f}  
    **F1 Score:** {metrics["f1"]:.4f}  
    **ROC AUC:** {metrics["roc_auc"]:.4f}  
    """)

    return metrics, model



# CLASSIFICATION REPORT
@app.cell
def _(metrics):
    mo.md("### Classification Report")
    print(metrics["report"])
    return


# SAVE FINAL MODEL
@app.cell
def _(MODEL_SAVE_PATH, SAVE_MODEL, model, scaler):
    if SAVE_MODEL:
        joblib.dump({"model": model, "scaler": scaler}, MODEL_SAVE_PATH)
        mo.md("Model saved successfully!")
    return


if __name__ == "__main__":
    app.run()

