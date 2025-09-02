from fastapi import APIRouter, Body, Depends
from app.core.enviroment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger


router = APIRouter()
logger = get_logger()

@router.get("/")
async def getLoadArtifact(name_rep: str, config: AppConfig = Depends(load_config)):
    logger.info("Execute Request - getLoadArtifact")
    try:
        print("Teste")
    except Exception as e:
        print("Teste")
        # logger.error(e)
