class SignupGatewayError(Exception):
    """Base class for JWT validation errors"""
    message_key = "signup_invalid_register"  # default
    status_code = 500

    def __init__(self, *args):
        super().__init__(*args)


class ExternalServiceError(SignupGatewayError):
    message_key = "external_service_error"
    status_code = 502


class InvalidGenerationToken(SignupGatewayError):
    message_key = "invalid_generation_token"
    status_code = 401


class InvalidToken(SignupGatewayError):
    message_key = "invalid_token"
    status_code = 401


class InvalidUserDataError(SignupGatewayError):
    message_key = "invalid_user_data"
    status_code = 400


class ResourceNotFoundError(SignupGatewayError):
    message_key = "resource_not_found"
    status_code = 404


class UserAlreadyExistsError(SignupGatewayError):
    message_key = "user_already_exists"
    status_code = 409


class InvalidCSRF(SignupGatewayError):
    message_key = "csrf_token"
    status_code = 401


class ExternalServiceError(SignupGatewayError):
    message_key = "external_service_error"
    status_code = 502


class InvalidCaptcha(SignupGatewayError):
    message_key = "captch_token"
    status_code = 403


class RegisterUserFailed(SignupGatewayError):
    message_key = "register_user_fail"
    status_code = 502


class SignupGatewaySuccess(Exception):
    """Base class for JWT validation errors"""
    message_key = "register_user_success"  # default
    status_code = 200


class GenerationToken(SignupGatewaySuccess):
    message_key = "generation_token"
    status_code = 200


class RegisterUserSuccess(SignupGatewaySuccess):
    message_key = "register_user_success"
    status_code = 200
