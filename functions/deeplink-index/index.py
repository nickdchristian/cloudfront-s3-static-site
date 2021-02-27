import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request = event["Records"][0]["cf"]["request"]

    old_uri = request["uri"]
    if old_uri.endswith("/"):
        new_uri = old_uri.replace(old_uri, "%sindex.html" % old_uri)

        logger.info("Old URI: %s" % old_uri)
        logger.info("New URI: %s" % new_uri)

        request["uri"] = new_uri

    return request
