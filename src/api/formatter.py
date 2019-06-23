import json
from typing import Dict

from logging import getLogger
from flask import Response

from src.api.errors import ERROR_MESSAGES

logger = getLogger(__name__)


def generate_error(data: Dict, error_code: int) -> Dict:
    if error_code not in ERROR_MESSAGES:
        logger.critical("Error message for code %d doest not exists" % error_code)
        message = ERROR_MESSAGES[0]
    else:
        message = ERROR_MESSAGES[error_code].format(**data)

    return {
        'error_code': error_code,
        'message': message
    }


def format_response(data: Dict, status: int = None, error_code: int = None) -> Response:
    if not error_code:
        return Response(
            response=json.dumps(data),
            status=status or 200,
            mimetype='application/json'
        )

    return Response(
        status=status or 400,
        response=json.dumps(generate_error(data, error_code)),
        mimetype='application/json'
    )
