# CI/CD pipeline

## Continuous Integration (CI)
* Trigger:
The CI starts running automatically when you push or pull code to the main branch.
* Pytest:
Run all the unit tests from that tests/ folder just to make sure nothing is broken.
* Type Checking:
pyright checks all our Python type hints.

## Continuous Deployment (CD)
* Trigger:
Deployment initiates automatically upon a successful merge into the main branch.
* Environment:
Targets the Azure Function App.
* Setup:
The deployment workflow file was automatically generated during the initial Azure setup.
* Mechanism:
CD is enabled, pulling the latest artifacts directly from the GitHub repository for service updates.
