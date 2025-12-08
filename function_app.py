import azure.functions as func
import logging
from prediction import make_prediction

app = func.FunctionApp()

# ------------- HELPERS ----------------------

def convert_contract(months: int):
    if months <= 1:
        return 0, 0
    elif months <= 12:
        return 1, 0
    else:
        return 0, 1

def convert_internet(service: str):
    service = service.lower().strip()
    return (
        1 if service == "fiber optic" else 0,
        1 if service == "no" else 0,
    )

def convert_payment(method: str):
    method = method.lower().strip()
    return (
        1 if method == "credit card (automatic)" else 0,
        1 if method == "electronic check" else 0,
        1 if method == "mailed check" else 0,
    )

# ------------- ROUTE ------------------------

@app.route(route="predict", auth_level=func.AuthLevel.FUNCTION)
def predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing prediction request...")

    try:
        tenure = float(req.params.get("tenure"))
        monthly = float(req.params.get("monthly"))
        techsupport = int(req.params.get("techsupport"))
        paperless = int(req.params.get("paperless"))

        contract_months = int(req.params.get("contract_months"))
        internet_service = req.params.get("internet_service")
        payment_method = req.params.get("payment_method")
    except Exception:
        return func.HttpResponse("Missing or invalid parameters", status_code=400)

    # --- One-hot encoders ---
    c_one, c_two = convert_contract(contract_months)
    i_fiber, i_no = convert_internet(internet_service)
    p_card, p_echeck, p_mail = convert_payment(payment_method)

    # --- Predict ---
    prob = make_prediction(
        **{
            "tenure": tenure,
            "MonthlyCharges": monthly,
            "TechSupport_yes": techsupport,
            "Contract_one year": c_one,
            "Contract_two year": c_two,
            "PaperlessBilling_yes": paperless,
            "InternetService_fiber optic": i_fiber,
            "InternetService_no": i_no,
            "PaymentMethod_credit card (automatic)": p_card,
            "PaymentMethod_electronic check": p_echeck,
            "PaymentMethod_mailed check": p_mail,
        }
    )

    return func.HttpResponse(str(prob), status_code=200)
