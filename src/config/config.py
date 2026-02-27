from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[1]
env_path = BASE_DIR / ".env"

load_dotenv(override=True)

class Config:
     # SETTINGS
     DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
     
     # TELEGRAM
     TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
     BOT_USERNAME = os.getenv("BOT_USERNAME")

     # PATHs
     SCRIPTS_PATH = Path(os.getenv("SCRIPTS_PATH", str(BASE_DIR / "scripts")))
     LOGS_PATH    = Path(os.getenv("LOGS_PATH",    str(BASE_DIR / "logs")))
     DOCS_PATH    = Path(os.getenv("DOCS_PATH",    str(BASE_DIR / "docs")))	
     TESTS_PATH   = Path(os.getenv("TESTS_PATH", str(BASE_DIR / "tests")))

     def __post_init__(self):
         """Выводит информацию о загрузке конфигурации только в консоль (не в файлы логов)"""
         print("\033[36m→ Загрузка конфигурации...\033[0m")
 
         print("\033[32m  ✓ Конфигурация загружена\033[0m")
         print(f"  • DEBUG          : {self.DEBUG}")
         print(f"  • TELEGRAM_TOKEN : {'установлен' if self.TELEGRAM_TOKEN else '\033[33mОТСУТСТВУЕТ\033[0m'}")
         print(f"  • BOT_USERNAME   : {self.BOT_USERNAME or '\033[33mне указан\033[0m'}")
         print(f"  • Логи будут в   : {self.LOGS_PATH}")
 
         if not self.TELEGRAM_TOKEN:
             print("\033[31m  ! Внимание: TELEGRAM_TOKEN отсутствует → бот не сможет работать\033[0m")
         
         print("")

config = Config()
config.__post_init__()
