from loguru import logger
from pathlib import Path
import sys

from src.config.config import config

def setup_logging():
    # Убираем дефолтный логгер loguru
    logger.remove()

    # ==========================
    # Консольный лог (цветной)
    # ==========================
    logger.add(
        sys.stdout,
        level="DEBUG" if config.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
        enqueue=True,
        catch=True,
    )

    # ==========================
    # Лог в файл с ротацией
    # ==========================
    logger.add(
        config.LOGS_PATH / "bot.log", 
        rotation="10 MB", 
        retention="14 days", 
        compression="zip", 
        level="DEBUG" if config.DEBUG else "INFO", 
        encoding="utf-8", 
        enqueue=True,
        # filter=lambda record: record["level"].name in ["INFO", "DEBUG", "WARNING"]  
)

    # ==========================
    # Лог в файл с ротацией
    # ==========================
    logger.add(
        config.LOGS_PATH / "errors.log",
        level="ERROR",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        enqueue=True,
        filter=lambda r: r["level"].name in ["ERROR", "CRITICAL"],
    )

     # ────────────────────────────────────────────────
     # 4. JSON-логи только в production (если понадобится для мониторинга)
     # ────────────────────────────────────────────────
     if not config.DEBUG:
         logger.add(
             config.LOGS_PATH / "bot.jsonl",
             format="{time} | {level} | {message}",
             serialize=True,
             rotation="500 MB",
             retention="90 days",
             level="INFO",
             enqueue=True,
    )    

    logger.success("логирование успешно инициализировано ✓")
    logger.info("Уровень консоли  : {}", "DEBUG" if config.DEBUG else "INFO")
    logger.info("Путь к логам     : {}", config.LOGS_PATH)

    return logger

# ==========================
# Singleton logger
# ==========================
logger = setup_logging()

# Удобные алиасы
log = logger
