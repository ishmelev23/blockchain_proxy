from flask import Blueprint, request
from logging import getLogger

from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED, ERROR_FUNCTION_INVALID_FIELDS, \
    ERROR_FUNCTION_CALL, ERROR_TRANSACTION_DB_SAVE
from src.api.formatter import format_response
from src.api.forms import NAME2FORM

logger = getLogger(__name__)
blueprint = Blueprint('transactions', __name__)


def send_transaction(data: dict) -> str:
    return '123'


def save_transaction(trx_hash: str):
    pass


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

    try:
        trx_hash = send_transaction(request.json)
    except Exception as e:
        logger.critical("Can't propagate data to blockchain!")
        return format_response(data={}, error_code=ERROR_FUNCTION_CALL)

    try:
        save_transaction(request.json)
    except Exception as e:
        logger.critical("Can't save data to local database. Transaction with hash %s is not tracking!" % trx_hash)
        return format_response(data={'trx_hash': trx_hash}, error_code=ERROR_TRANSACTION_DB_SAVE)

    return format_response(data={'trx_hash': trx_hash})


@blueprint.route('/transactions/<string:trx_hash>', methods=['GET'])
def transactions_get(trx_hash: str):
    return ''
