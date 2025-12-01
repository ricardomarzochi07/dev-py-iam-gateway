from typing import Optional, Dict, Any
from functools import lru_cache
import httpx
from jose import jwt
from jose.utils import base64url_decode

ALGORITHMS = ["RS256"]  # ajusta si tu IdP usa otro


@lru_cache(maxsize=1)
def fetch_jwks(jwks_url: str) -> Dict[str, Any]:
    # Cachea el JWKS en memoria (1 entrada). Puedes invalidar si rota la clave.
    with httpx.Client(timeout=5) as client:
        resp = client.get(jwks_url)
        resp.raise_for_status()
        return resp.json()


def pick_jwk_for_token(jwks: Dict[str, Any], kid: str) -> Dict[str, Any]:
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    raise ValueError("No se encontró la clave pública (kid) para validar el token.")


def validate_id_token(
        id_token: str,
        issuer: str,
        client_id: str,
        jwks_url: str,
        nonce_expected: Optional[str] = None,
        leeway_seconds: int = 120,
) -> Dict[str, Any]:
    """
    Valida firma y claims de un id_token OIDC.
    Retorna los 'claims' (payload) si todo es válido; levanta excepción si no.
    """
    # 1) Tomar el header para obtener el 'kid'
    header = jwt.get_unverified_header(id_token)
    kid = header.get("kid")
    alg = header.get("alg")
    if alg not in ALGORITHMS:
        raise ValueError(f"Algoritmo no permitido: {alg}")

    # 2) Obtener la JWK correcta
    jwks = fetch_jwks(jwks_url)
    jwk = pick_jwk_for_token(jwks, kid)

    # 3) Decodificar/verificar firma + claims estándar
    claims = jwt.decode(
        id_token,
        jwk,  # jose acepta dict JWK
        algorithms=ALGORITHMS,
        audience=client_id,
        issuer=issuer,
        options={
            "verify_aud": True,
            "verify_signature": True,
            "verify_exp": True,
            "verify_iat": True,
            "verify_nbf": True,
            "require_exp": True,
            "require_iat": True,
            "require_sub": True,
        },
    )

    # 4) Validaciones adicionales OIDC
    # aud múltiple ⇒ azp debe existir y ser tu client_id
    aud = claims.get("aud")
    if isinstance(aud, list) and len(aud) > 1:
        azp = claims.get("azp")
        if azp != client_id:
            raise ValueError("Claim 'azp' inválido para aud múltiple.")

    # nonce (si aplicaba PKCE/authorize con nonce)
    if nonce_expected is not None:
        if claims.get("nonce") != nonce_expected:
            raise ValueError("Nonce inválido en id_token.")

    return claims
