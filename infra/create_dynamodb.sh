#!/usr/bin/env bash
set -e
STACK_NAME=habit-tracker-table
TEMPLATE_FILE=dynamodb-cfn.yml

if ! command -v aws >/dev/null 2>&1; then
  echo "aws CLI not found. Install and configure AWS CLI with credentials first."
  exit 1
fi

aws cloudformation deploy --stack-name $STACK_NAME --template-file $TEMPLATE_FILE --capabilities CAPABILITY_NAMED_IAM
echo "DynamoDB table deployed (or already present)."
