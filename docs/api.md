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
Class Customer(Basemodel):
    tenure: int
    MonthlyCharges: int
    TechSupport_yes: int
    Contract_one year: int
    Contract_two year: int
    PaperlessBilling_yes: int
    InternetService_fiber optic: int
    InternetService_no: int
    PaymentMethod_credit card (automatic): int
    PaymentMethod_electronic check: int
    PaymentMethod_mailed check: int
```
