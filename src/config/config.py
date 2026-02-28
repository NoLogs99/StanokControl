import os
import sys
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from mashumaro.mixins.dict import DataClassDictMixin
    from mashumaro.config import BaseConfig
    _HAS_MASHUMARO = True
except Exception:
    _HAS_MASHUMARO = False

try:
    import msgspec as _msgspec
    _HAS_MSGSPEC = True
except Exception:
    _HAS_MSGSPEC = False

CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

# Описываем типы
ConfigFields = {
    "DEBUG": bool,
    "TELEGRAM_TOKEN": str,
    "BOT_USERNAME": str,
    "DATABASE_URL": str,
    "DATABASE_ANON_KEY": str, # Добавлено
    "SCRIPTS_PATH": Path,
    "LOGS_PATH": Path,
    "DOCS_PATH": Path,
    "TESTS_PATH": Path,
}

if _HAS_MSGSPEC:
    class Config(_msgspec.Struct):
        DEBUG: bool
        TELEGRAM_TOKEN: str
        BOT_USERNAME: str
        DATABASE_URL: str
        DATABASE_ANON_KEY: str # Добавлено
        SCRIPTS_PATH: str
        LOGS_PATH: str
        DOCS_PATH: str
        TESTS_PATH: str

    def _make_config_from_raw(raw: dict) -> Config:
        return Config(**raw)

elif _HAS_MASHUMARO:
    @dataclass(frozen=True, slots=True)
    class Config(DataClassDictMixin):
        DEBUG: bool
        TELEGRAM_TOKEN: str
        BOT_USERNAME: str
        DATABASE_URL: str
        DATABASE_ANON_KEY: str # Добавлено
        SCRIPTS_PATH: Path
        LOGS_PATH: Path
        DOCS_PATH: Path
        TESTS_PATH: Path

        class Meta(BaseConfig):
            lazy_compilation = True

    def _make_config_from_raw(raw: dict) -> Config:
        return Config.from_dict(raw)

else:
    @dataclass(frozen=True, slots=True)
    class Config:
        DEBUG: bool
        TELEGRAM_TOKEN: str
        BOT_USERNAME: str
        DATABASE_URL: str
        DATABASE_ANON_KEY: str # Добавлено
        SCRIPTS_PATH: Path
        LOGS_PATH: Path
        DOCS_PATH: Path
        TESTS_PATH: Path

    def _make_config_from_raw(raw: dict) -> Config:
        raw2 = raw.copy()
        for k, t in ConfigFields.items():
            if t is Path:
                raw2[k] = Path(raw2[k])
        return Config(**raw2)


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
            "DATABASE_ANON_KEY": get_env("DATABASE_ANON_KEY"), # Читаем из .env
            "SCRIPTS_PATH": os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts")),
            "LOGS_PATH": os.getenv("LOGS_PATH", str(BASE_DIR / "logs")),
            "DOCS_PATH": os.getenv("DOCS_PATH", str(BASE_DIR / "docs")),
            "TESTS_PATH": os.getenv("TESTS_PATH", str(BASE_DIR / "tests")),
        }

        cfg = _make_config_from_raw(raw_data)

        if _HAS_MSGSPEC:
            class _Wrapped:
                def __init__(self, inner):
                    self._inner = inner
                    self.DATABASE_URL = inner.DATABASE_URL
                    self.DATABASE_ANON_KEY = inner.DATABASE_ANON_KEY # Пробрасываем в обертку
                    self.SCRIPTS_PATH = Path(inner.SCRIPTS_PATH)
                    self.LOGS_PATH = Path(inner.LOGS_PATH)
                    self.DOCS_PATH = Path(inner.DOCS_PATH)
                    self.TESTS_PATH = Path(inner.TESTS_PATH)
                    self.DEBUG = inner.DEBUG
                    self.TELEGRAM_TOKEN = inner.TELEGRAM_TOKEN
                    self.BOT_USERNAME = inner.BOT_USERNAME

                def __repr__(self):
                    return f"Config(msgspec wrapped, DEBUG={self.DEBUG})"

            return _Wrapped(cfg)

        return cfg

    except Exception as e:
        print(f"❌ CRITICAL ERROR при валидации конфига: {e}")
        sys.exit(1)

config = load_config()
