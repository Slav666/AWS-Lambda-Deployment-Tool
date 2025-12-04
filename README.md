# AWS Lambda Deployment Tool (Python + boto3)

A simple but production-ready deployment tool for AWS Lambda.  
It packages Lambda code into a ZIP file, uploads the code to AWS,
publishes a new version, and updates/creates an alias.

## Features
- Automatic ZIP packaging
- Update existing Lambda or create a new one
- Publish new Lambda version
- Manage alias (e.g., `prod`)
- Zero manual AWS Console clicks

## Requirements
- Python 3.10+
- AWS credentials configured (`aws configure`)
- boto3

## Usage
1. Fill in your IAM role ARN inside `deploy.py`
2. Run:
