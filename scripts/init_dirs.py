import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

from src.config.config import config

def init_folders():
    folders = [
        # PATHs
        f'{config.LOGS_PATH}',
        f'{config.DOCS_PATH}',
        f'{config.SCRIPTS_PATH}',
        f'{config.TESTS_PATH}']        

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    print("✅ Все папки созданы!")

if __name__ == "__main__":
    init_folders()
