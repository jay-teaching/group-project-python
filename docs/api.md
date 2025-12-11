# Application Programing Interface

Our api is nice and easy to use. Here's how:

## Data Model

Here is our Pydantic data model. Our API supports these params:

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
```
