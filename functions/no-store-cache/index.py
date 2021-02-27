def handler(event, context):
    response = event["Records"][0]["cf"]["response"]
    response["headers"]["cache-control"] = [
        {
            "key": "Cache-Control",
            "value": "no-store",
        }
    ]
    return response
