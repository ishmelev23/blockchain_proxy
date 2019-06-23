
ERROR_INTERNAL_SERVER_ERROR = 0
ERROR_CONTRACT_NOT_SUPPORTED = 100
ERROR_FUNCTION_NOT_SUPPORTED = 101
ERROR_FUNCTION_INVALID_FIELDS = 102

ERROR_MESSAGES = {
    ERROR_INTERNAL_SERVER_ERROR: "Internal server error",
    ERROR_CONTRACT_NOT_SUPPORTED: "Contract '{contract_name}' does not supported",
    ERROR_FUNCTION_NOT_SUPPORTED: "Function '{func_name} for contract '{contract_name}' doest not supported",
    ERROR_FUNCTION_INVALID_FIELDS: "Function call data contains errors: {errors}"

}