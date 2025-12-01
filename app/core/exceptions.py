# exceptions.py
class OperationStatus(Exception):
    """Base class for application errors with i18n message keys."""
    message_key = "unknown_error"
    status_code = 500

    def __init__(self, message_key: str | None = None, status_code: int | None = None):
        super().__init__(message_key or self.message_key)
        if message_key:
            self.message_key = message_key
        if status_code:
            self.status_code = status_code


class ExternalServiceError(OperationStatus):
    message_key = "external_service_error"
    status_code = 502


class InvalidUserDataError(OperationStatus):
    message_key = "invalid_user_data"
    status_code = 400


class InvalidGenerationToken(OperationStatus):
    message_key = "invalid_generation_token"
    status_code = 401  # podría ser 400 si el formato es inválido


class CodeExchangeError(OperationStatus):
    message_key = "code_exchange"
    status_code = 400  # podría ser 400 si el formato es inválido


class InvalidToken(OperationStatus):
    message_key = "invalid_token"
    status_code = 401


class InvalidUserDataError(OperationStatus):
    message_key = "invalid_user_data"
    status_code = 400


class ResourceNotFoundError(OperationStatus):
    message_key = "resource_not_found"
    status_code = 404


class UserAlreadyExistsError(OperationStatus):
    message_key = "user_already_exists"
    status_code = 409


class InvalidCSRF(OperationStatus):
    message_key = "csrf_invalid"
    status_code = 403  # más correcto que 401


class InvalidCaptcha(OperationStatus):
    message_key = "captcha_invalid"
    status_code = 403


class InvalidPreLogin(OperationStatus):
    message_key = "prelogin_invalid"
    status_code = 403  # más correcto que 401


class RegisterUserFailed(OperationStatus):
    message_key = "register_user_failed"
    status_code = 502  # o 500 si el fallo es interno
