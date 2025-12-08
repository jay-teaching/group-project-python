import prediction


def test_make_prediction_simple():
    args = {
        "tenure": 2,
        "MonthlyCharges": 12.3,
        "TechSupport_yes": 0,
        "Contract_one year": 0,
        "Contract_two year": 0,
        "PaperlessBilling_yes": 1,
    }
    result = prediction.make_prediction(**args)
    assert isinstance(result, float)

