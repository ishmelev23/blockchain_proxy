from flask import Blueprint

blueprint = Blueprint('transactions', __name__)


@blueprint.route('/contracts/<string:contract_name>/transactions', methods=['POST'])
def transactions_create(contract_name: str):
    return ''


@blueprint.route('/transactions/<string:trx_hash>', methods=['GET'])
def transactions_get(trx_hash: str):
    return ''
