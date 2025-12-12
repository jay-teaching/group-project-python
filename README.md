# Telco Customer Churn Prediction

## Project Summary

Customer churn is a critical business problem for telecommunications companies. Losing a customer is significantly more expensive than retaining one. This project delivers a machine learning solution that predicts which customers are likely to churn, enabling proactive retention strategies.

We built and deployed a logistic regression model using the IBM Telco Customer Churn dataset (which can be found on [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)). The solution includes a REST API backend and an interactive web frontend, deployed on Azure Container Apps for scalability.

---

## Business Value

By identifying at-risk customers before they leave telecom providers can:

- Target retention offers to the right customers
- Reduce customer acquisition costs
- Improve customer lifetime value
- Make data-driven decisions about service improvements

---

## Model and Features

We use a logistic regression model as specified in the assignment. The model uses 11 engineered features to improve predictive accuracy. These engineered features es were made up from the following original variables:

- `tenure`: Customer tenure in months
- `MonthlyCharges`: Monthly charges billed to the customer
- `TechSupport_yes`: 1 if the customer has tech support, 0 otherwise
- `Contract`: Either monthly(1m), yearly(12m), or bi-yearly (24m). Our frontend accepts any value in months but converts it to the lengt hclosest to one of these three values
- `PaperlessBilling_yes`: 1 if the customer uses paperless billing, 0 otherwise
- `InternetService`: Internet service option chosen by customer. Can be either fiber optic internet, DSL, or none
- `PaymentMethod`: User:s payment method. Can be a bank transfer, credit card, electronic check, or mailed check

These features are derived from the original dataset and one-hot encoded for use in the model. The model predicts the probability of customer churn based on these inputs.

### Model Performance

- Accuracy: approximately 80%
- ROC AUC: between 0.84-0.87
- Balanced precision and recall for business use

---

## System Architecture

The application follows a simple architecture:

1. Frontend: Streamlit was used as the interactive web interface where users input customer attributes and receive churn predictions
2. Backend: FastAPI used as the REST endpoint that processes requests and returns predictions
3. Machine Learning Model: Trained logistic regression model served via the API

The backend is containerized using Docker and deployed to Azure Container Apps for automatic scaling and a public URL. The frontend (Streamlit app) is running in the virtual machine and can be accessed at: [http://131.163.96.16:8501/](http://131.163.96.16:8501/)

The budget was limited to the given limit of $25/month from an Azure student account.

![Azure Budget](azure_budget.png)

---

## Interactive Frontend

We built a Streamlit-based web application that:

- Adjusts customer attributes using sliders and dropdowns
- Submits predictions with a single click
- Displays results with clear risk interpretation: either high or low churn probability, with any figure above 20% being considered high

---

## How to Run Locally

### Prerequisites

- Python 3.12+
- uv package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/jay-teaching/group-project-python.git
cd group-project-python

# Set up environment
uv sync

# Start the backend
uv run uvicorn backend.main:app --port 8000

# In a new terminal, start the frontend (localhost only)
uv run streamlit run frontend/app.py

# To allow access from any IP address (e.g., for cloud or VM deployments):
uv run streamlit run frontend/app.py --server.address=0.0.0.0
```

---

## How to Test the API

- API docs (Swagger UI):
  - Codespaces: After forwarding port 8000, use your unique forwarded address (see PORTS tab) and add `/docs` to the end. Example: `https://<your-codespace-id>-8000.app.github.dev/docs`
  - Local: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Production: [https://telco-backend.politeriver-aee86836.norwayeast.azurecontainerapps.io/docs](https://telco-backend.politeriver-aee86836.norwayeast.azurecontainerapps.io/docs)
- You can test the prediction endpoint directly in your browser using these docs.

> **Note for Codespaces users:**
> Each user will have a unique forwarded address for port 8000. After starting the backend, forward port 8000 in the PORTS tab, then click the link and add `/docs` to access the Swagger UI.
>
> Tip: After starting the backend, Codespaces may auto-forward port 8000. If you don't see it in the PORTS tab, click "Add Port" and enter 8000. Then use the forwarded address with `/docs` to access the Swagger UI.

---

## Deployment

- Backend is deployed with Azure Container Apps using Docker.
- All deployment configuration and Dockerfiles are included in the repository.

---

## How to Deploy the Backend as an Azure Function (Serverless)

1. **Set Up Azure Functions in Your Codespace**
   - Install the Azure Functions extension in VS Code.
   - Open the Command Palette (`Ctrl+Shift+P`), type and select: `Azure Functions: Create Function`.
   - Choose Python as the language, HTTP trigger as the template, and provide a function name (e.g., `predict`).
   - Set the authorization level to `Function`.

2. **Prepare Your Code**
   - Use the provided `function_app.py` as your main function file.
   - Ensure your `requirements.txt` includes `azure-functions` and all other dependencies:
     ```bash
     uv add azure-functions
     uv pip freeze > requirements.txt
     ```
   - Make sure your model file and any dependencies are included in the deployment folder.

3. **Deploy to Azure**
   - In the Azure Portal, create a new Azure Function App (Python 3.12+).
   - Choose the Flex Consumption plan for cost efficiency.
   - Enable Continuous Deployment and link your GitHub repo if desired.
   - Deploy your code using the Azure Functions extension or GitHub Actions.

4. **Test the Function**
   - In the Azure Portal, go to your Function App and select your function.
   - Use the Test/Run feature or send an HTTP request to the function’s public URL with the required parameters (e.g., `tenure`, `monthly`, `techsupport`, etc.).
   - You should receive a prediction result.

5. **Update the Frontend**
   - Set the `API_URL` in your frontend to the Azure Function’s public HTTP endpoint, e.g.:
     ```python
     API_URL = "https://<your-function-app-name>.azurewebsites.net/api/predict"
     ```

> **Note:** With this approach, you do not need to run or manage your own VM. Azure Functions will handle scaling and availability for you, and you only pay for what you use.

---

## Project Structure

```text
group-project-python/
├── backend/main.py          # FastAPI REST API
├── frontend/app.py          # Streamlit web interface
├── prediction.py            # Core prediction logic
├── models/                  # Trained model files
├── notebooks/               # Model training notebook
├── tests/                   # Unit tests
├── Dockerfile.backend       # Container configuration
└── requirements.txt         # Dependencies
```

---

## Tech Stack

- Dataset: IBM Telco Customer Churn Dataset
- Cloud Platform: Microsoft Azure
- Frameworks: FastAPI, Streamlit, scikit-learn, UV, Marimo, pytest, Docker, Uvicorn
