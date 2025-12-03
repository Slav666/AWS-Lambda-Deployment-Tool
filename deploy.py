import boto3
import zipfile
import os
import io

FUNCTION_NAME = "my-deployed-lambda"
ALIAS_NAME = "prod"
RUNTIME = "python3.12"
ROLE_ARN = "arn:aws:iam::471112899084:role/lambda-execution-role"

lambda_client = boto3.client("lambda")


def zip_lambda_code(source_dir):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder, _, files in os.walk(source_dir):
            for file in files:
                filepath = os.path.join(folder, file)
                arcname = os.path.relpath(filepath, source_dir)
                zf.write(filepath, arcname)
    buffer.seek(0)
    return buffer.read()


def create_or_update_function(zip_bytes):
    try:
        print("Updating Lambda function…")
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_bytes,
            Publish=True
        )
        return response["Version"]

    except lambda_client.exceptions.ResourceNotFoundException:
        print("Function not found, creating a new one…")
        response = lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler="lambda_function.lambda_handler",
            Code={"ZipFile": zip_bytes},
            Publish=True
        )
        return response["Version"]


def update_alias(version):
    try:
        lambda_client.update_alias(
            FunctionName=FUNCTION_NAME,
            Name=ALIAS_NAME,
            FunctionVersion=version
        )
        print(f"Alias '{ALIAS_NAME}' updated → version {version}")
    except lambda_client.exceptions.ResourceNotFoundException:
        lambda_client.create_alias(
            FunctionName=FUNCTION_NAME,
            Name=ALIAS_NAME,
            FunctionVersion=version
        )
        print(f"Alias '{ALIAS_NAME}' created → version {version}")


if __name__ == "__main__":
    print("Zipping lambda code…")
    code = zip_lambda_code("lambda_function")

    print("Deploying to AWS Lambda…")
    version = create_or_update_function(code)

    print(f"Published new version: {version}")

    print("Updating alias…")
    update_alias(version)

    print("Deployment complete ✔")
