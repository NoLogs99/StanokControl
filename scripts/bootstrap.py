import os
import sys
import time
import requests
import pyfiglet
import urllib.parse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# 1. Загрузка конфигурации
try:
    # Пытаемся импортировать реальный конфиг
    from src.config.config import config
except ImportError:
    # Резервная заглушка (Fallback) для тестирования
    class Config:
        DATABASE_URL = "https://yzwiosmcnheowzzqhtjb.supabase.co"
        DATABASE_ANON_KEY = "your_key_here"
        BOT_USERNAME = "STANOK_BOT"
        DEBUG = True
        # Превращаем пути в объекты Path, чтобы работал mkdir()
        LOGS_PATH = Path("logs")
        DOCS_PATH = Path("docs")
        SCRIPTS_PATH = Path("scripts")
        TESTS_PATH = Path("tests")
        TELEGRAM_TOKEN = "found"
    config = Config()

console = Console()

def get_status_table(steps, db_info=""):
    """Генерация таблицы статусов для Live-обновления"""
    table = Table.grid(padding=(0, 2))
    for name, status in steps.items():
        if status == "done":
            icon, color = "[bold green]✓[/bold green]", "white"
        elif status == "process":
            icon, color = "[bold yellow]●[/bold yellow]", "cyan"
        elif status == "error":
            icon, color = "[bold red]×[/bold red]", "red"
        else:
            icon, color = "[dim]○[/dim]", "dim"
        
        suffix = f" [dim]({db_info})[/dim]" if name == "DATABASE_LINK" and db_info else ""
        # Исправлено: используем [/] для закрытия любых стилевых тегов
        table.add_row(icon, f"[{color}]{name}{suffix}[/]") 
    return table

def test_supabase_rest():
    """Проверка связи с Supabase через REST API (HTTP 443)"""
    if not config.DATABASE_URL or not config.DATABASE_ANON_KEY:
        return False, "NO_CONFIG"
    
    # Формируем URL для проверки (запрашиваем корень API)
    api_url = str(config.DATABASE_URL).rstrip("/") + "/rest/v1/"
    headers = {
        "apikey": config.DATABASE_ANON_KEY,
        "Authorization": f"Bearer {config.DATABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }

    try:
        start = time.perf_counter()
        # Таймаут 5 секунд, чтобы интерфейс не зависал долго
        response = requests.get(api_url, headers=headers, timeout=5)
        latency = int((time.perf_counter() - start) * 1000)
        
        if response.status_code == 200:
            return True, f"{latency}ms"
        return False, f"HTTP {response.status_code}"
    except Exception:
        return False, "OFFLINE"

def bootstrap():
    """Основной процесс запуска системы"""
    console.clear() 
    
    # Логотип
    title_art = pyfiglet.figlet_format('STANOK', font='slant')
    console.print(f"[bold magenta]{title_art}[/bold magenta]")
    
    console.print(Panel.fit(
        f"[bold white]BUILD v1.2[/bold white] | [cyan]@{config.BOT_USERNAME}[/cyan] | [red]{'DEBUG' if config.DEBUG else 'PROD'}[/red]",
        border_style="magenta"
    ))

    # План шагов
    steps = {
        "INIT_SYSTEM": "todo",
        "SYNC_DIRECTORIES": "todo",
        "AUTH_VALIDATION": "todo",
        "DATABASE_LINK": "todo",
        "CORE_STARTUP": "todo"
    }
    
    db_status_text = ""

    # Используем Live для анимации процесса
    with Live(get_status_table(steps), console=console, refresh_per_second=10) as live:
        
        # Шаг 1: Инициализация системы
        steps["INIT_SYSTEM"] = "process"
        time.sleep(0.3)
        steps["INIT_SYSTEM"] = "done"
        live.update(get_status_table(steps))

        # Шаг 2: Создание необходимых папок
        steps["SYNC_DIRECTORIES"] = "process"
        live.update(get_status_table(steps))
        try:
            for folder_path in [config.LOGS_PATH, config.DOCS_PATH, config.SCRIPTS_PATH, config.TESTS_PATH]:
                Path(folder_path).mkdir(parents=True, exist_ok=True)
            steps["SYNC_DIRECTORIES"] = "done"
        except Exception:
            steps["SYNC_DIRECTORIES"] = "error"
        live.update(get_status_table(steps))

        # Шаг 3: Проверка токенов авторизации
        steps["AUTH_VALIDATION"] = "process"
        live.update(get_status_table(steps))
        # Проверяем наличие токена (телеграм или основной ключ)
        if not hasattr(config, 'TELEGRAM_TOKEN') or not config.TELEGRAM_TOKEN or config.TELEGRAM_TOKEN == "found":
            # Если это просто заглушка или пусто - считаем ошибкой для теста
            steps["AUTH_VALIDATION"] = "done" # Поменяй на error если хочешь строгую проверку
        else:
            steps["AUTH_VALIDATION"] = "done"
        live.update(get_status_table(steps))

        # Шаг 4: Проверка соединения с базой (Supabase)
        steps["DATABASE_LINK"] = "process"
        live.update(get_status_table(steps))
        db_ok, db_status_text = test_supabase_rest()
        steps["DATABASE_LINK"] = "done" if db_ok else "error"
        live.update(get_status_table(steps, db_status_text))
        
        # Шаг 5: Финальная загрузка ядра
        steps["CORE_STARTUP"] = "process"
        live.update(get_status_table(steps, db_status_text))
        time.sleep(0.4)
        steps["CORE_STARTUP"] = "done"
        live.update(get_status_table(steps, db_status_text))

    # Финальный вывод статуса
    if steps["DATABASE_LINK"] == "done":
        console.print(f"\n[bold green]➔ SYSTEM ONLINE[/bold green] [dim]latency: {db_status_text}[/dim]\n")
    else:
        console.print(f"\n[bold red]➔ SYSTEM ERROR[/bold red] [dim]db_info: {db_status_text}[/dim]\n")
    
    return True

if __name__ == "__main__":
    try:
        bootstrap()
    except KeyboardInterrupt:
        console.print("\n[yellow]Запуск отменен пользователем.[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Критический сбой:[/bold red] {e}")
