import json
from typing import Optional

from flask import Blueprint, request, Response
from logging import getLogger

from sqlalchemy.orm import Session

from src.api.errors import ERROR_CONTRACT_NOT_SUPPORTED, ERROR_FUNCTION_NOT_SUPPORTED, ERROR_FUNCTION_INVALID_FIELDS, \
     ERROR_TRANSACTION_DB_SAVE, ERROR_TRANSACTION_NOT_EXISTS, ERROR_DATABASE_CONNECTION
from src.api.formatter import format_response
from src.api.forms import NAME2FORM
from src.database.session import session_scope_func
from src.database.models.transaction import Transaction

logger = getLogger(__name__)
blueprint = Blueprint('transactions', __name__)


@session_scope_func
def save_transaction(session: Session, contract_name: str, func_name: str, data: dict) -> id:
    trx = Transaction(contract_name=contract_name, func_name=func_name, data=json.dumps(data))
    session.add(trx)
    session.flush()
    return trx.id


@session_scope_func
def get_transaction(session: Session, pk: int) -> Optional[dict]:
    trx = session.query(Transaction).get(pk)
    if trx:
        return trx.dict
    return None


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
        pk = save_transaction(contract_name, func_name, form.contract_data)
    except:
        logger.exception("Can't save transaction to database! With data %s" % form.data)
        return format_response(data={}, error_code=ERROR_TRANSACTION_DB_SAVE)

    return format_response(data={'id': pk})


@blueprint.route('/transactions/<int:pk>', methods=['GET'])
def transactions_get(pk: int) -> Response:
    try:
        trx = get_transaction(pk)
    except:
        logger.exception("Error during connection to database!")
        return format_response(data={}, error_code=ERROR_DATABASE_CONNECTION)

    if not trx:
        return format_response(data={'pk': pk}, error_code=ERROR_TRANSACTION_NOT_EXISTS)

    return format_response(data=trx)
