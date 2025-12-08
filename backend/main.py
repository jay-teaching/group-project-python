from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prediction import make_prediction

app = FastAPI(
    title="Telco Churn API",
    description="FastAPI backend for churn prediction",
    version="1.0.0",
)

class PredictionRequest(BaseModel):
    tenure: float
    monthly: float
    techsupport: int
    paperless: int
    contract_months: int
    internet_service: str
    payment_method: str

def convert_contract(months):
    if months <= 1:
        return 0, 0
    elif months <= 12:
        return 1, 0
    else:
        return 0, 1

def convert_internet(service):
    s = service.lower().strip()
    return (
        1 if s == "fiber optic" else 0,
        1 if s == "no" else 0,
    )

def convert_payment(method):
    m = method.lower().strip()
    return (
        1 if m == "credit card (automatic)" else 0,
        1 if m == "electronic check" else 0,
        1 if m == "mailed check" else 0,
    )

@app.post("/predict")
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
