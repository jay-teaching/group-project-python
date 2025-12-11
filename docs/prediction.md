# Great Prediction

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
def predict(data: PredictionRequest):

    c1, c2 = convert_contract(data.contract_months)
    i_fiber, i_no = convert_internet(data.internet_service)
    p_card, p_echeck, p_mail = convert_payment(data.payment_method)

    try:
        prob = make_prediction(
            **{
                "tenure": data.tenure,
                "MonthlyCharges": data.monthly,
                "TechSupport_yes": data.techsupport,
                "Contract_one year": c1,
                "Contract_two year": c2,
                "PaperlessBilling_yes": data.paperless,
                "InternetService_fiber optic": i_fiber,
                "InternetService_no": i_no,
                "PaymentMethod_credit card (automatic)": p_card,
                "PaymentMethod_electronic check": p_echeck,
                "PaymentMethod_mailed check": p_mail,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"churn_probability": prob}
```
