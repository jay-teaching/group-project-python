# Prediction

Our prediction model is excellent to predict Telco Churn Probability. Here's how:

## Prediction Model

Our prediciton model uses 11 factors to predict customers' behaviors:

* `tenure`
* `MonthlyCharges`
* `TechSupport_yes`
* `Contract_one year`
* `Contract_two year`
* `PaperlessBilling_yes`
* `InternetService_fiber optic`
* `InternetService_no`
* `PaymentMethod_credit card (automatic)`
* `PaymentMethod_electronic check`
* `PaymentMethod_mailed check`

```python
def make_prediction(**kwargs: float) -> float:
    """Make a churn prediction given the input features."""

    try:
        # Ensure all features exist
        _ = [kwargs[feature] for feature in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e.args[0]}") from e

    # Build DataFrame from a typed dict instead of a list
    row = {feature: kwargs[feature] for feature in FEATURE_ORDER}
    df = pd.DataFrame([row])

    # Scale features
    scaled = SCALER.transform(df)

    # Predict probability
    prob = float(MODEL.predict_proba(scaled)[0, 1])

    print(f"Churn probability: {prob:.4f}")
    return prob
```
