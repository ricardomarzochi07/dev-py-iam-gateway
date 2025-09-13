from buddybet_logmon_common.logger import get_logger

from app.client.signup_core_service.signup_core_request_schema import SignupCoreRequestSchema
from app.core.environment_config import AppConfig
from app.core.iam_constants import IAMConstants
import httpx
import time



class SignupCoreServiceClient:
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env

    def post_register_user(self, data: SignupCoreRequestSchema, access_token: str):
        self.logger.info("Execute Request - get_token_oidc")
''' 
        url = self.env_var.signup_register_service_url
        headers = {"Authorization": f"Bearer {access_token}"}

        # Call OIDC_Service for get new Token - WSO2
        for attempt in range(1, IAMConstants.RETRIES + 1):
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url, headers=headers, json=data.dict())
                    response.raise_for_status()  # Lanza excepción si status >= 400
                    return response
            except httpx.RequestError as exc:
                print(f"[Intento {attempt}] Error de conexión: {exc}")
                self.logger.error(f"[Intento {attempt}] Error de conexión", exc_info=True)

            except httpx.HTTPStatusError as exc:
                print(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}")
                self.logger.error(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}", exc_info=True)
            if attempt < IAMConstants.RETRIES:
                time.sleep(IAMConstants.DELAY)
        # devuelve None si falla después de todos los retries
        return None
'''
