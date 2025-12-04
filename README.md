# Habit Tracker — Perfect (No Login)

This version:
- No login (per-browser anonymous ID)
- Colorful responsive UI
- In-memory backend by default (safe for demo)
- Optional DynamoDB support when USE_DYNAMODB=1 and AWS creds provided

Run with Docker (recommended):
docker compose up --build

Or build and run:
docker build -t habit-perfect .
docker run --rm -p 5000:5000 -e USE_DYNAMODB=0 habit-perfect

Or run locally with Python 3.11 venv:
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main


## GitHub CI
A GitHub Actions workflow is included at `.github/workflows/ci.yml` that runs tests and builds a Docker image.

## DynamoDB Infra
CloudFormation and Terraform examples are included in the `infra/` folder. Use `infra/create_dynamodb.sh` to deploy the CloudFormation stack (requires AWS CLI configured).
