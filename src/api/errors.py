
ERROR_INTERNAL_SERVER_ERROR = 0
ERROR_CONTRACT_NOT_SUPPORTED = 100
ERROR_FUNCTION_NOT_SUPPORTED = 101
ERROR_FUNCTION_INVALID_FIELDS = 102
ERROR_FUNCTION_CALL = 103
ERROR_TRANSACTION_DB_SAVE = 104
ERROR_TRANSACTION_NOT_EXISTS = 105
ERROR_DATABASE_CONNECTION = 105

ERROR_MESSAGES = {
    ERROR_INTERNAL_SERVER_ERROR: "Internal server error",
    ERROR_CONTRACT_NOT_SUPPORTED: "Contract '{contract_name}' does not supported",
    ERROR_FUNCTION_NOT_SUPPORTED: "Function '{func_name} for contract '{contract_name}' doest not supported",
    ERROR_FUNCTION_INVALID_FIELDS: "Function call data contains errors: {errors}",
    ERROR_FUNCTION_CALL: "Failed to propagate data to blockchain",
    ERROR_TRANSACTION_DB_SAVE: "Failed to track transaction with hash {trx_hash} to database",
    ERROR_TRANSACTION_NOT_EXISTS: "Transaction with {trx_hash} isn't tracking by that server",
    ERROR_DATABASE_CONNECTION: "Problems during connection to database"
}