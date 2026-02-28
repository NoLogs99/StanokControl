import os
import sys
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
from urllib.parse import urlparse # Добавили для разбора DATABASE_URL

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
        """Парсит DATABASE_URL для драйвера pg8000"""
        try:
            p = urlparse(self.DATABASE_URL)
            return {
                "user": p.username,
                "password": p.password,
                "host": p.hostname,
                "port": p.port or 5432,
                "database": p.path.lstrip('/'),
            }
        except Exception:
            return {}

    if _HAS_MASHUMARO:
        class Meta(BaseConfig):
            lazy_compilation = True

def load_config() -> Config:
    def get_env(key: str, default: str = None) -> str:
        val = os.getenv(key, default)
        if not val or val.strip() == "":
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
            "SCRIPTS_PATH": Path(os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts"))),
            "LOGS_PATH": Path(os.getenv("LOGS_PATH", str(BASE_DIR / "logs"))),
            "DOCS_PATH": Path(os.getenv("DOCS_PATH", str(BASE_DIR / "docs"))),
            "TESTS_PATH": Path(os.getenv("TESTS_PATH", str(BASE_DIR / "tests"))),
        }

        return Config.from_dict(raw_data) if _HAS_MASHUMARO else Config(**raw_data)

    except Exception as e:
        print(f"❌ CRITICAL ERROR при валидации конфига: {e}")
        sys.exit(1)

config = load_config()
