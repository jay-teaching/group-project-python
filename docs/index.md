# Welcome to PYTHON Group Project

This project developed a comprehensive predictive model powered by the IBM Telco Customer Churn dataset to identify and quantify potential customer flight risk, translating technical insights into a clear competitive advantage for retention strategy.

## Features

* Good looking **dashboard**
* [CI/CD pipeline](pipeline.md)
* Easy to use [API](api.md)
* Great [Prediction](prediction.md)
* Interactive [Streamlit](Streamlit.md)
* Reactive [Marimo Notebook](marimo_notebook.md)

## Project layout
 
    mkdocs.yml          # The configuration file.
    docs/
        index.md        # The documentation homepage.
        ...             # Other markdown pages, images and other files.
    main.py             # Set API with FastAPI
    telco_marimo.py     # Marimo notebook
    function_app.py     # Azure function definition
    prediction.py       # Prediction model
    app.py              # Set streamlit function

## Contributing


* Make prediction model successfully
* Wonderful streamlit and marimo
* CI pipeline runs automatically
* CD pipeline triggers automatically
* Deploys to Azure Function App
* Live service updated