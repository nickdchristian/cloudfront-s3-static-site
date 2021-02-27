import json
import logging
import os
from pathlib import Path

import yaml
from black import format_str, FileMode
from cfn_flip import to_json, to_yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CURRENT_PATH = Path(os.getcwd())


FORMAT_LAMBDA_FUNCTIONS = True
FORMAT_CLOUDFORMATION_TEMPLATES = True


def format_templates():
    """ Subjectively formats and sorts keys of CloudFormation templates written in YAML."""
    for subdir, dirs, files in os.walk((CURRENT_PATH.parent)):
        for file in files:
            if file.endswith("template.yaml") or file.endswith("template.yml"):
                with open(os.path.join(subdir, file), "r+") as template:
                    try:
                        formatted_json_template = to_json(template.read())
                        formatted_template = to_yaml(
                            json.dumps(
                                json.loads(formatted_json_template),
                                indent=4,
                                sort_keys=True,
                            ),
                            clean_up=True
                        )
                        template.seek(0)
                        template.write(formatted_template)
                        template.truncate()
                    except json.decoder.JSONDecodeError as e:
                        logger.error("Failed to format %s" % os.path.join(subdir, file))
                        raise e

                    logger.info("Formatted %s" % os.path.join(subdir, file))


def format_lambda_functions():
    """ Subjectively formats the lambda functions named 'index.py'. """
    for subdir, dirs, files in os.walk(CURRENT_PATH.parent):
        for file in files:
            if file == "index.py":
                with open(os.path.join(subdir, file), "r+") as python_file:
                    formatted_python = format_str(
                        python_file.read(), mode=FileMode(line_length=100)
                    )
                    python_file.seek(0)
                    python_file.write(formatted_python)
                    python_file.truncate()
                    logger.info("Formatted %s" % os.path.join(subdir, file))


def format():
    if FORMAT_CLOUDFORMATION_TEMPLATES:
        format_templates()
    if FORMAT_LAMBDA_FUNCTIONS:
        format_lambda_functions()


format()
