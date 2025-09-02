from fastapi import FastAPI
from app.api.v1.endpoints import gateway_iam_controller
from buddybet_logmon_common.fastapi_logger import setup_fastapi_logging

app = FastAPI()
setup_fastapi_logging(app)

app.include_router(gateway_iam_controller.router, prefix="/gateway_iam", tags=["gateway-iam"])
