import os
import yaml
from functools import lru_cache
from app.core.environment_config import AppConfig, AppConfigEnvironment
from pathlib import Path
import re
from cryptography.hazmat.primitives import serialization
from app.core.iam_constants import IAMConstants
from app.dto.keys_dto import KeysDTO


def expand_env_variables(content: str) -> str:
    # Reemplaza ${VAR} por el valor real de os.environ["VAR"]
    return re.sub(r'\$\{([^}]+)}', lambda m: os.getenv(m.group(1), ""), content)


@lru_cache()
def load_config():
    app_env = os.getenv("APP_ENV")
    with open(Path(f"resources/env_{app_env}.yaml"), "r") as f:
        content = f.read()
    expand_content = expand_env_variables(content)
    data = yaml.safe_load(expand_content)

    # Cargar keys
    keys = get_keys(app_env)
    # Extraer diccionario interno
    signup_env_data = data.get("signup_gateway_env", {}).copy()
    signup_env_data["public_key"] = keys.public_key

    # Crear AppConfigEnvironment
    signup_env = AppConfigEnvironment(**signup_env_data)
    return AppConfig(signup_gateway_env=signup_env)


def get_keys(app_env: str):
    match app_env:
        case IAMConstants.LOCAL_ENV:
            return KeysDTO(
                private_key=None,
                public_key=open_file_public_dev(app_env))
        case IAMConstants.PRE_ENV:
            print("Env PRE")
            return None
        case IAMConstants.PROD_ENV:
            print("Env PRO")
            return None
        case _:
            raise ValueError(f"Entorno desconocido: {app_env}")


def open_file_public_dev(app_env: str):
    key_path = Path(f"resources/certs/public_key_{app_env}.pem")
    try:
        with open(key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        return public_key_bytes
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de clave public: {key_path}")
    except ValueError as e:
        raise ValueError(f"Error cargando la clave public: {e}")
