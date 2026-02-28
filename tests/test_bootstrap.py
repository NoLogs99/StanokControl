import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from dataclasses import replace
import scripts.bootstrap as bs

def test_init_folders(tmp_path, monkeypatch):
    """Проверка создания директорий через подмену путей в конфиге."""
    # Создаем копию конфига с временными путями (replace работает с frozen dataclasses)
    test_root = tmp_path / "app_data"
    mock_config = replace(
        bs.config,
        LOGS_PATH=test_root / "logs",
        DOCS_PATH=test_root / "docs",
        SCRIPTS_PATH=test_root / "scripts",
        TESTS_PATH=test_root / "tests"
    )
    
    # Подменяем весь объект config в модуле bootstrap
    monkeypatch.setattr(bs, "config", mock_config)
    
    mock_logger = MagicMock()
    from scripts.bootstrap import init_folders
    init_folders(mock_logger)
    
    assert mock_config.LOGS_PATH.exists()
    assert (test_root / "scripts").is_dir()

def test_bootstrap_missing_token(monkeypatch):
    """Проверка реакции на отсутствие токена (обходим frozen dataclass)."""
    mock_logger = MagicMock()
    
    # 1. Создаем "битый" конфиг через replace
    bad_config = replace(bs.config, TELEGRAM_TOKEN=None, BOT_USERNAME=None)
    
    # 2. Подменяем зависимости
    monkeypatch.setattr(bs, "config", bad_config)
    monkeypatch.setattr("scripts.bootstrap.setup_logging", lambda x: mock_logger)
    monkeypatch.setattr("scripts.bootstrap.init_folders", lambda x: None)
    
    from scripts.bootstrap import bootstrap
    bootstrap()
    
    # 3. Проверяем, что ошибка залогирована
    errors = "".join([str(c) for c in mock_logger.error.call_args_list])
    assert "TELEGRAM_TOKEN" in errors
    assert "BOT_USERNAME" in errors

def test_bootstrap_success_logic(monkeypatch):
    """Проверка успешного пути."""
    mock_logger = MagicMock()
    # Создаем валидный конфиг
    good_config = replace(bs.config, TELEGRAM_TOKEN="123:ABC", BOT_USERNAME="@bot")
    
    monkeypatch.setattr(bs, "config", good_config)
    monkeypatch.setattr("scripts.bootstrap.setup_logging", lambda x: mock_logger)
    monkeypatch.setattr("scripts.bootstrap.init_folders", lambda x: None)
    
    from scripts.bootstrap import bootstrap
    conf, _ = bootstrap()
    
    assert conf.TELEGRAM_TOKEN == "123:ABC"
    # Проверяем вызов success
    success_msgs = "".join([str(c) for c in mock_logger.success.call_args_list])
    assert "Все обязательные переменные" in success_msgs

@pytest.mark.parametrize("attr", ["LOGS_PATH", "DOCS_PATH", "SCRIPTS_PATH"])
def test_config_is_path_obj(attr):
    """Проверка, что пути — это Path."""
    path_val = getattr(bs.config, attr)
    assert isinstance(path_val, Path)
