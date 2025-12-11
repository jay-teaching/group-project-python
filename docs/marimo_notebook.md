# Reactive Marimo Notebook

By utilizing an interactive input form to gather customer data, the dashboard  facilitates real-time predictions via the underlying FastAPI architecture. The results are then analyzed, offering a distinct visual representation of churn likelihood.

## Marimo Notebook Function

```python
@app.cell
def _(MODEL_SAVE_PATH, SAVE_MODEL, model, scaler):
    if SAVE_MODEL:
        joblib.dump({"model": model, "scaler": scaler}, MODEL_SAVE_PATH)
        mo.md("Model saved successfully!")
    return


if __name__ == "__main__":
    app.run()
```
## Run Marimo Notebook

```python
marimo run notebooks/telco_marimo.py
marimo edit notebooks/telco_marimo.py
```