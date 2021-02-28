import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """Redirects from a www subdomain to the base domain."""
    
    request = event["Records"][0]["cf"]["request"]

    logger.info(request)
    if request["headers"]["host"][0]["value"].startswith("www"):
        redirect_domain = request["headers"]["host"][0]["value"].replace("www.", "")
        logger.info("https://%s%s" % (redirect_domain, request["uri"]))
        return {
            "status": "302",
            "statusDescription": "Found",
            "headers": {
                "location": [
                    {
                        "key": "Location",
                        "value": "https://%s%s" % (redirect_domain, request["uri"]),
                    }
                ]
            },
        }
    return request
