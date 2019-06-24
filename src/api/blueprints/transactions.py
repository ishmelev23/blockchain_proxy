import random

from flask import Blueprint, request, Response
from logging import getLogger

from sqlalchemy.orm import Session

from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED, ERROR_FUNCTION_INVALID_FIELDS, \
    ERROR_FUNCTION_CALL, ERROR_TRANSACTION_DB_SAVE, ERROR_TRANSACTION_NOT_EXISTS, ERROR_DATABASE_CONNECTION
from src.api.formatter import format_response
from src.api.forms import NAME2FORM
from src.database.session import session_scope_func
from src.database.models.transaction import Transaction

logger = getLogger(__name__)
blueprint = Blueprint('transactions', __name__)


def send_transaction(address: str, abi: str, func_name: str, data: dict) -> str:
    return ''.join([random.choice('0123456789ABCDEF') for i in range(64)])


@session_scope_func
def save_transaction(session: Session, trx_hash: str):
    trx = Transaction(trx_hash=trx_hash)
    session.add(trx)


@session_scope_func
def get_transaction(session: Session, trx_hash: str) -> dict:
    trx = session.query(Transaction).filter(Transaction.trx_hash == trx_hash).one_or_none()
    if trx:
        return trx.dict
    return trx


@blueprint.route('/contracts/<string:contract_name>/<string:func_name>', methods=['POST'])
def transactions_create(contract_name: str, func_name: str) -> Response:
    if contract_name not in NAME2FORM:
        logger.error("Form for contract_name '%s' does not exists" % contract_name)
        return format_response(data={'contract_name': contract_name}, error_code=ERROR_CONTRACT_NOT_SUPPORTED)

    contract = NAME2FORM[contract_name]
    form_class = contract.get(func_name)
    if not form_class:
        return format_response(data={'contract_name': contract_name, 'func_name': func_name},
                               error_code=ERROR_FUNCTION_NOT_SUPPORTED)

    form = form_class(request.form)
    if not form.validate():
        return format_response(data={'errors': form.errors}, error_code=ERROR_FUNCTION_INVALID_FIELDS)

    try:
        trx_hash = send_transaction(contract['address'], contract['abi'], form.func_name, request.json)
    except:
        logger.exception("Can't propagate data to blockchain!")
        return format_response(data={}, error_code=ERROR_FUNCTION_CALL)

    try:
        save_transaction(trx_hash)
    except:
        logger.exception("Can't save transaction with trx_hash %s to database!" % trx_hash)
        return format_response(data={'trx_hash': trx_hash}, error_code=ERROR_TRANSACTION_DB_SAVE)

    return format_response(data={'trx_hash': trx_hash})


@blueprint.route('/transactions/<string:trx_hash>', methods=['GET'])
def transactions_get(trx_hash: str) -> Response:
    try:
        trx = get_transaction(trx_hash)
    except:
        logger.exception("Error during connection to database!")
        return format_response(data={}, error_code=ERROR_DATABASE_CONNECTION)

    if not trx:
        return format_response(data={'trx_hash': trx_hash}, error_code=ERROR_TRANSACTION_NOT_EXISTS)

    return format_response(data=trx)
