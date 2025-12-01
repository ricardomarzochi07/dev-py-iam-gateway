class IAMConstants:
    DEFAULT_EXP_MINUTES = 2
    ALGORITHM = "RS256"
    TOKEN_TYPE = "Bearer"
    RETRIES = 3
    DELAY = 2.0
    AUDIENCE = "SignupUser"
    LOCAL_ENV = "local"
    DEV_ENV = "dev"
    PRE_ENV = "pre"
    PROD_ENV = "prod"
    SESSION_COOKIE_NAME = "BFF_SESSION"
    SESSION_TTL_SECONDS = 3600  #1h