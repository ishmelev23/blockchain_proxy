from flask import Blueprint, request
from logging import getLogger

from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED, ERROR_FUNCTION_INVALID_FIELDS
from src.api.formatter import format_response
from src.api.forms import NAME2FORM

logger = getLogger(__name__)
blueprint = Blueprint('transactions', __name__)


@blueprint.route('/contracts/<string:contract_name>/<string:func_name>', methods=['POST'])
def transactions_create(contract_name: str, func_name: str):
    if contract_name not in NAME2FORM:
        logger.error("Form for contract_name '%s' does not exists" % contract_name)
        return format_response(data={'contract_name': contract_name}, error_code=ERROR_CONTRACT_NOT_SUPPORTED)

    form_class = NAME2FORM[contract_name].get(func_name)
    if not form_class:
        return format_response(data={'contract_name': contract_name, 'func_name': func_name},
                               error_code=ERROR_FUNCTION_NOT_SUPPORTED)

    form = form_class(request.form)
    if not form.validate():
        return format_response(data={'errors': form.errors}, error_code=ERROR_FUNCTION_INVALID_FIELDS)

    return format_response(data={})


@blueprint.route('/transactions/<string:trx_hash>', methods=['GET'])
def transactions_get(trx_hash: str):
    return ''
