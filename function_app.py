import azure.functions as func
import logging
from prediction import make_prediction

# Convert contract length (in months) into one-hot features
def convert_contract_to_features(months: int):
    if months <= 1:
        return 0, 0
    elif months <= 12:
        return 1, 0
    else:
        return 0, 1

app = func.FunctionApp()

@app.route(route="predict", auth_level=func.AuthLevel.FUNCTION)
def predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing prediction request.")

    try:
        tenure = float(req.params.get("tenure"))
        monthly = float(req.params.get("monthly"))
        techsupport = int(req.params.get("techsupport"))
        contract_months = int(req.params.get("contract_months"))
        paperless = int(req.params.get("paperless"))
    except (TypeError, ValueError):
        return func.HttpResponse(
            "Missing or invalid parameters.",
            status_code=400
        )

    # Convert contract months → one-hot encoding
    contract_one_year, contract_two_year = convert_contract_to_features(contract_months)

    # Run model prediction
    prediction = make_prediction(
        **{
            "tenure": tenure,
            "MonthlyCharges": monthly,
            "TechSupport_yes": techsupport,
            "Contract_one year": contract_one_year,
            "Contract_two year": contract_two_year,
            "PaperlessBilling_yes": paperless,
        }
    )

    return func.HttpResponse(
        str(prediction),
        status_code=200
    )
