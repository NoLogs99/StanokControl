import pytest
from unittest.mock import MagicMock
from src.utils.logger import setup_logging
from src.config.config import config

def test_logger_levels(caplog):
    """Проверка, что логгер фиксирует сообщения разных уровней."""
    # 1. Инициализируем логгер (он обычно возвращает объект loguru или стандартный)
    logger = setup_logging(config)

    # 2. Пишем логи разных уровней
    # Мы используем caplog.at_level, чтобы pytest перехватил поток
    with caplog.at_level("DEBUG"):
        logger.info("Test INFO message")
        logger.error("Test ERROR message")
        logger.debug("Test DEBUG message")

    # 3. Проверяем наличие текста в перехваченных логах
    assert "Test INFO message" in caplog.text
    assert "Test ERROR message" in caplog.text
    
    # Если DEBUG в конфиге выключен, это сообщение может не попасть в лог
    if config.DEBUG:
        assert "Test DEBUG message" in caplog.text

def test_logger_success_method():
    """Проверка специфических методов (например, .success в Loguru)."""
    logger = setup_logging(config)
    
    # Если логгер самописный или Loguru, проверяем наличие метода success
    assert hasattr(logger, "success"), "Логгер должен поддерживать метод .success()"
    
    # Проверяем, что вызов метода не вызывает исключений
    try:
        logger.success("Success message check")
    except Exception as e:
        pytest.fail(f"Метод logger.success() упал с ошибкой: {e}")

def test_logger_formatting():
    """Проверка форматирования строк (через {}) в логгере."""
    logger = setup_logging(config)
    
    # Проверяем, что логгер умеет подставлять значения в скобки {}
    # Если это loguru, это работает из коробки. 
    # Если стандартный logging, может потребоваться проверка.
    try:
        logger.info("Value: {}", "test_value")
    except Exception:
        # Если упало, значит логгер ожидает %s или f-строки
        pytest.fail("Логгер не поддерживает форматирование через {}")

@pytest.mark.parametrize("level", ["info", "warning", "error", "critical", "debug", "success"])
def test_all_logger_methods_exist(level):
    """Авто-тест на наличие всех стандартных методов логгирования."""
    logger = setup_logging(config)
    assert hasattr(logger, level), f"У логгера отсутствует метод {level}"
