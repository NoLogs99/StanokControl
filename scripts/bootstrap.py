from pathlib import Path

from src.config.config import config
from src.utils.logger import setup_logging


def init_folders(logger):
    """
    Создание необходимых директорий проекта
    """
    folders = [
        config.LOGS_PATH,
        config.DOCS_PATH,
        config.SCRIPTS_PATH,
        config.TESTS_PATH,
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)

    logger.success("Все рабочие директории инициализированы")


def bootstrap():
    # Инициализация логгера
    logger = setup_logging(config)

    logger.success("Приложение запускается")
    # logger.info("DEBUG      : {}", config.DEBUG)
    # logger.info("LOGS_PATH  : {}", config.LOGS_PATH)

    # Создание папок
    init_folders(logger)

    # Проверка обязательных данных
    missing = []

    if not config.TELEGRAM_TOKEN:
        missing.append("TELEGRAM_TOKEN")

    if not config.BOT_USERNAME:
        missing.append("BOT_USERNAME")

    if missing:
        logger.error("Отсутствуют обязательные переменные: {}", ", ".join(missing))
    else:
        logger.success("Все обязательные переменные окружения загружены ✓")

    return config, logger
