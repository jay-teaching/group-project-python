import prediction


def test_make_prediction_simple():
    args = {
        "tenure": 10,
        "MonthlyCharges": 70.5,
        "TechSupport_yes": 1,
        "Contract_one year": 0,
        "Contract_two year": 1,
        "PaperlessBilling_yes": 1,
        "InternetService_fiber optic": 1,
        "InternetService_no": 0,
        "PaymentMethod_credit card (automatic)": 0,
        "PaymentMethod_electronic check": 1,
        "PaymentMethod_mailed check": 0,
    }

    result = prediction.make_prediction(**args)
    assert isinstance(result, float)
