#!/bin/bash
set -e
mkdir -p docs/reports
echo "Running flake8..."
flake8 app || true
echo "Running bandit..."
bandit -r app -o docs/reports/bandit_report.json -f json || true
echo "Running safety..."
safety check -r requirements.txt --full-report > docs/reports/safety_report.txt || true
echo "Reports are in docs/reports/"
