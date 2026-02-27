from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / ".env"

load_dotenv(override=True)

class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME")

    SCRIPTS_PATH = Path(os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts")))
    LOGS_PATH = Path(os.getenv("LOGS_PATH", str(BASE_DIR / "logs")))
    DOCS_PATH = Path(os.getenv("DOCS_PATH", str(BASE_DIR / "docs")))
    TESTS_PATH = Path(os.getenv("TESTS_PATH", str(BASE_DIR / "tests")))


config = Config()
