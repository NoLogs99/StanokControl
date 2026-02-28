import pytest
from pathlib import Path
from src.config.config import config

def test_config_loader():
    """Проверка, что конфиг загружен корректно и данные валидны."""
    
    # 1. Базовые типы данных
    assert isinstance(config.DEBUG, bool), "DEBUG должен быть True/False"
    assert isinstance(config.TELEGRAM_TOKEN, str), "Токен должен быть строкой"
    assert len(config.TELEGRAM_TOKEN) > 10, "Токен подозрительно короткий"
    
    # 2. Логика полей
    # assert config.BOT_USERNAME.startswith('@'), "Username бота должен начинаться с @"
    
    # 3. Работа с путями (Pathlib)
    path = config.SCRIPTS_PATH
    assert isinstance(path, Path), "SCRIPTS_PATH должен быть объектом Path из pathlib"
    
    # Если путь относительный (как 'scripts'), pytest может его не найти без resolve()
    # Проверяем существование папки физически
    assert path.exists(), f"Директория {path} не найдена. Сейчас путь: {path.absolute()}"
    assert path.is_dir(), f"Объект {path} должен быть папкой, а не файлом"

@pytest.mark.parametrize("attr, expected_type", [
    ("DEBUG", bool),
    ("TELEGRAM_TOKEN", str),
    ("BOT_USERNAME", str),
    ("SCRIPTS_PATH", Path),
    ("LOGS_PATH", Path),
    ("DOCS_PATH", Path),
    ("TESTS_PATH", Path),
])
def test_config_structure(attr, expected_type):
    """Автоматическая проверка всех полей конфига на наличие и тип."""
    assert hasattr(config, attr), f"В конфиге пропущено обязательное поле: {attr}"
    assert isinstance(getattr(config, attr), expected_type), f"Поле {attr} имеет неверный тип"

def test_paths_are_writeable():
    """Проверка, что в папки из конфига можно записывать файлы (важно для логов и скриптов)."""
    for path_attr in ["SCRIPTS_PATH", "LOGS_PATH"]:
        path = getattr(config, path_attr)
        # Проверяем права на запись, если папка существует
        if path.exists():
            assert os.access(path, os.W_OK), f"Нет прав на запись в директорию {path_attr}"

import os # импорт для теста прав доступа
