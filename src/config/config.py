import os
import sys
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
from mashumaro.mixins.dict import DataClassDictMixin

# Настройка путей проекта
CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent.parent

# Загружаем .env
load_dotenv(override=True)

@dataclass(frozen=True, slots=True)
class Config(DataClassDictMixin):
    DEBUG: bool
    TELEGRAM_TOKEN: str
    BOT_USERNAME: str
    SCRIPTS_PATH: Path
    LOGS_PATH: Path
    DOCS_PATH: Path
    TESTS_PATH: Path

def _get_env_or_fail(key: str) -> str:
    """Гарантирует наличие переменной, иначе завершает работу."""
    value = os.getenv(key)
    if not value:
        print(f"❌ CRITICAL ERROR: '{key}' не установлен в .env")
        sys.exit(1)
    return value.strip()

def load_config() -> Config:
    try:
        # Собираем данные в словарь для Mashumaro
        raw_data = {
            "DEBUG": os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
            "TELEGRAM_TOKEN": _get_env_or_fail("TELEGRAM_TOKEN"),
            "BOT_USERNAME": _get_env_or_fail("BOT_USERNAME"),
            
            # Если в .env пути нет, берем дефолтный путь от корня проекта
            "SCRIPTS_PATH": os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts")),
            "LOGS_PATH": os.getenv("LOGS_PATH", str(BASE_DIR / "logs")),
            "DOCS_PATH": os.getenv("DOCS_PATH", str(BASE_DIR / "docs")),
            "TESTS_PATH": os.getenv("TESTS_PATH", str(BASE_DIR / "tests")),
        }

        # Mashumaro конвертирует строки в Path и проверяет типы
        return Config.from_dict(raw_data)

    except Exception as e:
        print(f"❌ CRITICAL ERROR при загрузке конфига: {e}")
        sys.exit(1)

# Экспортируем готовый объект
config = load_config()
