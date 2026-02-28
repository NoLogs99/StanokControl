# bootstrap.py
import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Optional

# Импорты с graceful fallback'ом
try:
    import pyfiglet
except Exception:
    pyfiglet = None

try:
    import plotext as plt
except Exception:
    plt = None

try:
    from InquirerPy import inquirer
except Exception:
    inquirer = None

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.align import Align
    from rich import box
    from rich.text import Text
    from rich.rule import Rule
except Exception:
    print("Требуется библиотека rich. Установи: python -m pip install rich")
    raise

try:
    from loguru import logger
except Exception:
    # лёгкий фоллбек на print
    class _Logger:
        def info(self, *a, **k): print("[INFO]", *a)
        def error(self, *a, **k): print("[ERROR]", *a)
        def debug(self, *a, **k): print("[DEBUG]", *a)
    logger = _Logger()

# Console и пути
console = Console()
BASE_DIR = Path.cwd()
SCRIPTS_PATH = Path(os.getenv("SCRIPTS_PATH", BASE_DIR / "scripts"))

# Удобные helper'ы
def ascii_title(text: str) -> str:
    if pyfiglet:
        try:
            return pyfiglet.figlet_format(text, font="slant")
        except Exception:
            pass
    # fallback
    return f"=== {text} ==="

def simple_menu(choices):
    """Фолбэк-меню через input"""
    console.print("Выбери опцию:")
    for i, c in enumerate(choices, 1):
        console.print(f"  {i}. {c}")
    while True:
        sel = input("> ").strip()
        if not sel:
            return None
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        console.print("[red]Неверный ввод, введи номер опции.[/red]")

def show_header():
    console.clear()
    title = ascii_title("ULTRA CLI")
    console.print(f"[bold magenta]{title}[/bold magenta]")
    console.print(Rule(style="grey37"))

def simulate_startup():
    logger.info("Инициализация модулей...")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Загрузка библиотек...", total=100)
        for i in range(0, 101, 10):
            progress.update(task, advance=10)
            time.sleep(0.12)
    logger.info("Готово.")

def show_stats():
    table = Table(title="Состояние системы", box=box.SIMPLE_HEAVY, expand=False)
    table.add_column("Параметр", style="cyan", no_wrap=True)
    table.add_column("Значение", style="green")
    table.add_row("Статус", "[bold green]ONLINE[/bold green]")
    table.add_row("CPU Load", "24%")
    table.add_row("Uptime", "154:12:01")
    table.add_row("Memory", "1.3 GB / 4 GB")
    console.print(Panel(table, border_style="yellow"))

def plot_graph():
    y = [1, 5, 3, 8, 4, 9, 12, 7]
    title = "Акции Газмяса"
    if plt:
        try:
            plt.clear_figure()
        except Exception:
            try:
                plt.clf()
            except Exception:
                pass
        plt.plot(y, marker="filled")
        plt.title(title)
        plt.show()
        return
    # fallback: простой ASCII-график через rich
    maxv = max(y)
    rows = []
    for val in y:
        bar = "█" * int((val / maxv) * 30)
        rows.append((val, bar))
    t = Table(box=box.MINIMAL)
    t.add_column("index")
    t.add_column("value", justify="right")
    t.add_column("chart")
    for i, (val, bar) in enumerate(rows):
        t.add_row(str(i), str(val), bar)
    console.print(Panel(Align.center(t), title=title, border_style="cyan"))

def list_scripts() -> list:
    if not SCRIPTS_PATH.exists():
        return []
    return sorted([p for p in SCRIPTS_PATH.iterdir() if p.is_file() and os.access(p, os.X_OK)])

def run_script(path: Path):
    console.print(f"Запускаю [green]{path}[/green] ...")
    try:
        # выполняем в новом процессе, чтобы избежать конфликтов окружения
        res = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=60)
        console.print(Panel(f"[bold]Вывод:[/bold]\n{res.stdout or '(пусто)'}\n\n[bold]Ошибки:[/bold]\n{res.stderr or '(нет)'}", title=f"Результат {path.name}"))
    except subprocess.TimeoutExpired:
        console.print("[red]Скрипт превысил время выполнения[/red]")

def test_supabase_connection():
    """
    Тест простого REST-запроса к Supabase.
    Ожидает переменные окружения: SUPABASE_URL и SUPABASE_ANON_KEY.
    Попытается сделать GET к /rest/v1/<table>?limit=1
    """
    import json
    import urllib.parse
    import requests  # requests удобен и часто уже есть; если нет — сообщим

    supabase_url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    if not supabase_url or not anon_key:
        console.print("[red]Переменные SUPABASE_URL и SUPABASE_ANON_KEY должны быть в окружении (.env)[/red]")
        console.print("Пример: SUPABASE_URL=https://xyzabc.supabase.co")
        return

    # выбираем простую тестовую таблицу. Если у тебя нет таблицы, используй 'users' или создай test_table.
    table = input("Введите имя таблицы для теста (по умолчанию 'users'): ").strip() or "users"
    base = supabase_url.rstrip("/") + "/rest/v1"
    url = urllib.parse.urljoin(base + "/", f"{table}?select=*&limit=1")
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Accept": "application/json",
    }
    console.print(f"GET {url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        console.print(f"Status: {r.status_code}")
        try:
            data = r.json()
            console.print(Panel(json.dumps(data, ensure_ascii=False, indent=2), title="Response JSON", border_style="green"))
        except Exception:
            console.print(Panel(r.text, title="Response Text", border_style="yellow"))
    except Exception as e:
        console.print(f"[red]Ошибка запроса:[/red] {e}")

def main_loop():
    show_header()
    simulate_startup()

    choices = ["Показать статистику", "Построить график", "Скрипты", "Тест Supabase", "Выход"]
    while True:
        if inquirer:
            try:
                action = inquirer.select(message="Выбери режим работы:", choices=choices).execute()
            except Exception:
                action = simple_menu(choices)
        else:
            action = simple_menu(choices)

        if action == "Показать статистику":
            show_stats()
        elif action == "Построить график":
            plot_graph()
        elif action == "Скрипты":
            scripts = list_scripts()
            if not scripts:
                console.print("[yellow]Скриптов не найдено в SCRIPTS_PATH[/yellow]")
                continue
            script_choices = [p.name for p in scripts] + ["Назад"]
            if inquirer:
                sel = inquirer.select(message="Выбери скрипт:", choices=script_choices).execute()
            else:
                sel = simple_menu(script_choices)
            if sel and sel != "Назад":
                run_script(SCRIPTS_PATH / sel)
        elif action == "Тест Supabase":
            try:
                test_supabase_connection()
            except ModuleNotFoundError:
                console.print("[red]Требуется requests: python -m pip install requests[/red]")
        else:
            console.print("Пока! 👋")
            break

if __name__ == "__main__":
    main_loop()
