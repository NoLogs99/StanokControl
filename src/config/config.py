import os
import sys
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
from urllib.parse import urlparse  # 1. ОБЯЗАТЕЛЬНО ДОБАВИТЬ

try:
    from mashumaro.mixins.dict import DataClassDictMixin
    from mashumaro.config import BaseConfig
    _HAS_MASHUMARO = True
except ImportError:
    _HAS_MASHUMARO = False

CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent.parent

load_dotenv(override=True)

@dataclass(frozen=True, slots=True)
class Config(DataClassDictMixin if _HAS_MASHUMARO else object):
    DEBUG: bool
    TELEGRAM_TOKEN: str
    BOT_USERNAME: str
    DATABASE_URL: str
    DATABASE_ANON_KEY: str
    SCRIPTS_PATH: Path
    LOGS_PATH: Path
    DOCS_PATH: Path
    TESTS_PATH: Path

    @property
    def db_params(self) -> dict:
        """Распарсенные параметры для pg8000"""
        try:
            parsed = urlparse(self.DATABASE_URL)
            return {
                "user": parsed.username,
                "password": parsed.password,
                "host": parsed.hostname,
                "port": parsed.port or 5432,
                "database": parsed.path.lstrip('/'),
                "ssl_context": True  # Обязательно для Supabase
            }
        except Exception as e:
            print(f"❌ ERROR: Кривой DATABASE_URL: {e}")
            return {}

    if _HAS_MASHUMARO:
        class Meta(BaseConfig):
            # Включаем приведение типов (чтобы строки из env стали Path)
            # и ленивую компиляцию для скорости
            lazy_compilation = True

def load_config() -> Config:
    def get_env(key: str, default: str = None) -> str:
        val = os.getenv(key, default)
        if val is None or val.strip() == "":
            # Если переменной нет вообще - это критикал
            print(f"❌ CRITICAL ERROR: '{key}' не задан или пуст!")
            sys.exit(1)
        return val.strip()

    try:
        raw_data = {
            "DEBUG": os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
            "TELEGRAM_TOKEN": get_env("TELEGRAM_TOKEN"),
            "BOT_USERNAME": get_env("BOT_USERNAME"),
            "DATABASE_URL": get_env("DATABASE_URL"),
            "DATABASE_ANON_KEY": get_env("DATABASE_ANON_KEY"),
            "SCRIPTS_PATH": os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts")),
            "LOGS_PATH": os.getenv("LOGS_PATH", str(BASE_DIR / "logs")),
            "DOCS_PATH": os.getenv("DOCS_PATH", str(BASE_DIR / "docs")),
            "TESTS_PATH": os.getenv("TESTS_PATH", str(BASE_DIR / "tests")),
        }

        if _HAS_MASHUMARO:
            # Mashumaro сама превратит строки в Path объекты
            return Config.from_dict(raw_data)
        
        # Ручная сборка, если либы нет
        return Config(
            **{k: (Path(v) if "PATH" in k else v) for k, v in raw_data.items() if k != "DEBUG"},
            DEBUG=raw_data["DEBUG"]
        )

    except Exception as e:
        print(f"❌ CRITICAL ERROR при загрузке конфига: {e}")
        sys.exit(1)

# Инициализация
config = load_config()
