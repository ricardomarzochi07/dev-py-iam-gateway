from buddybet_logmon_common.logger import get_logger

from app.client.oidc_gateway_service.oidc_internal_schema_response import OidcInternalResponseSchema
from app.core.environment_config import AppConfig
from app.core.iam_constants import IAMConstants
from app.client.oidc_gateway_service.oidc_idp_schema_response import OidcIdpResponseSchema
import httpx
import time
from pydantic import ValidationError


class OidcGatewayServiceClient:
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.signup_gateway_env

    def get_token_oidc_idp(self, data) -> OidcIdpResponseSchema:
        self.logger.info("Execute Request - get_token_oidc_idp")

        url = self.env_var.oidc_idp_token_service_url
        print(" url >>>>>", url)
        headers = {"Content-Type": f"application/json"}

        # Call OIDC_Service for get new Token - WSO2
        for attempt in range(1, IAMConstants.RETRIES + 1):
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url, headers=headers, json=data.dict())
                    response.raise_for_status()  # Lanza excepción si status >= 400
                    print(" >>> response.raise_for_status() >>>>>", response.raise_for_status())

                    return OidcIdpResponseSchema(**response.json())
            except httpx.RequestError as exc:
                print(f"[Intento {attempt}] Error de conexión: {exc}")
                self.logger.error(f"[Intento {attempt}] Error de conexión", exc_info=True)

            except httpx.HTTPStatusError as exc:
                print(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}")
                self.logger.error(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}",
                                  exc_info=True)
                try:
                    error_data = exc.response.json()
                    print("Error details:", error_data)
                except ValueError:
                    print("No hay JSON en la respuesta de error.")
                    self.logger.error(f"No hay JSON en la respuesta de error.", exc_info=True)
            except ValidationError as exc:
                print(f"[Intento {attempt}] Error al parsear JSON en DTO: {exc}")
                self.logger.error(f"[Intento {attempt}] Error al parsear JSON en DTO:", exc_info=True)
                # Opcional: log o raise según necesites
            if attempt < IAMConstants.RETRIES:
                time.sleep(IAMConstants.DELAY)
        # devuelve None si falla después de todos los retries
        return None

    def get_token_oidc_internal(self) -> OidcInternalResponseSchema:
        self.logger.info("Execute Request - get_token_oidc_internal")

        url = self.env_var.oidc_internal_token_service_url
        headers = {"Accept": f"application/json"}

        # Call OIDC_Service for get new Token - WSO2
        for attempt in range(1, IAMConstants.RETRIES + 1):
            try:
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url, headers=headers)
                    response.raise_for_status()  # Lanza excepción si status >= 400
                    return OidcInternalResponseSchema(**response.json())
            except httpx.RequestError as exc:
                print(f"[Intento {attempt}] Error de conexión: {exc}")
                self.logger.error(f"[Intento {attempt}] Error de conexión", exc_info=True)

            except httpx.HTTPStatusError as exc:
                print(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}")
                self.logger.error(f"[Intento {attempt}] Error HTTP: {exc.response.status_code} - {exc.response.text}",
                                  exc_info=True)
                try:
                    error_data = exc.response.json()
                    print("Error details:", error_data)
                except ValueError:
                    print("No hay JSON en la respuesta de error.")
                    self.logger.error(f"No hay JSON en la respuesta de error.")
            except ValidationError as exc:
                print(f"[Intento {attempt}] Error al parsear JSON en DTO: {exc}")
                self.logger.error(f"[Intento {attempt}] Error al parsear JSON en DTO:")
                # Opcional: log o raise según necesites
            if attempt < IAMConstants.RETRIES:
                time.sleep(IAMConstants.DELAY)
        # devuelve None si falla después de todos los retries
        return None

