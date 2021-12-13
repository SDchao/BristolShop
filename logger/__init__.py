from loguru import logger

logger.add("runtime.log", rotation="10 MB", level="INFO", encoding="utf8")
