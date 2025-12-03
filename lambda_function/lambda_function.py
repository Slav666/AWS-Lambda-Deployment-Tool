def lambda_handler(event, context):
    return {
        "message": "Hello from deployed Lambda!",
        "event": event
    }
