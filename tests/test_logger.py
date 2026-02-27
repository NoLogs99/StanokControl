from src.utils.logger import setup_logging
from src.config.config import config

logger = setup_logging()

logger.info("Тестовый лог: Logger работает корректно")
logger.warning("Тестовый лог: Это предупреждение")
logger.error("Тестовый лог: Это ошибка")
logger.debug("Тестовый лог: Это отладочная информация (не будет отображаться в консоли)")   
logger.critical("Тестовый лог: Это критическая ошибка")
logger.success("Тестовый лог: Это сообщение об успехе")

logger.info("Application started")
logger.debug("DEBUG включен? {}", config.DEBUG)
