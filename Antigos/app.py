# app.py
# -----------------------------------------------------------
# Reabre o Chrome com o perfil de automação criado pelo login_once.py
# (USER DATA não-padrão), já autenticado no PJe, e executa ações.
# Gera logs em ./logs/app.log e screenshots em ./logs/.
# -----------------------------------------------------------

from playwright.sync_api import sync_playwright
from pathlib import Path
import logging
import sys
import time
import os

# === Caminhos devem bater com os usados no login_once.py ===
DST_USER_DATA_DIR = str(Path(os.getenv("LOCALAPPDATA", r"C:\Users\mario\AppData\Local")) / "ChromeAutomation" / "User Data")
DST_PROFILE_NAME  = "Default"

TARGET_URL = "https://pje.tjdft.jus.br/pje/ng2/dev.seam#/painel-usuario-interno"

LOG_DIR  = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%H:%M:%S [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console)
    logging.info("=== Início do app.py ===")
    logging.info(f"User Data (automação): {DST_USER_DATA_DIR} -> {DST_PROFILE_NAME}")

def open_logged_browser():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=DST_USER_DATA_DIR,
            channel="chrome",
            headless=False,
            locale="pt-BR",
            accept_downloads=True,
            args=[
                "--start-maximized",
                f"--profile-directory={DST_PROFILE_NAME}",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            ignore_default_args=[
                "--enable-automation",
                "--disable-extensions",
                "--no-sandbox",
            ],
        )

        # Preferimos reutilizar uma aba existente; se não houver, criamos
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.bring_to_front()
        except Exception:
            pass

        # Logs úteis
        page.on("console", lambda m: logging.info(f"[CONSOLE {m.type().upper()}] {m.text()}"))
        page.on("pageerror", lambda e: logging.error(f"[PAGEERROR] {e}"))
        page.on("requestfailed", lambda r: logging.error(f"[REQFAILED] {r.url} -> {getattr(r.failure, 'error_text', '')}"))

        return context, page

def goto(page, url, note, attempts=2):
    for i in range(1, attempts+1):
        try:
            logging.info(f"[NAV {i}/{attempts}] {note}: {url}")
            page.goto(url, wait_until="load", timeout=60000)
            logging.info("[NAV] OK")
            return True
        except Exception as e:
            logging.warning(f"[NAV] Falha: {e}")
            try:
                screenshot = LOG_DIR / f"app_nav_fail_{int(time.time())}.png"
                page.screenshot(path=str(screenshot))
                logging.info(f"[NAV] Screenshot: {screenshot}")
            except Exception:
                pass
            time.sleep(2)
    return False

def main():
    setup_logging()

    if not Path(DST_USER_DATA_DIR).exists():
        logging.error("Pasta do perfil de automação não encontrada. Rode primeiro o login_once.py.")
        sys.exit(1)

    context = None
    try:
        context, page = open_logged_browser()

        # Vá direto ao painel (se a sessão estiver válida, entra; se não, o PJe redireciona)
        ok = goto(page, TARGET_URL, "Abrindo painel do PJe")
        if not ok:
            logging.error("Não foi possível abrir o painel do PJe.")
            sys.exit(2)

        # Aguarde um pouco para o app Angular carregar áreas do painel
        time.sleep(4)

        # === EXEMPLO DE AÇÃO: capturar título/URL e fazer um screenshot ===
        try:
            title = page.title()
        except Exception:
            title = "(sem título)"
        logging.info(f"Página carregada: title='{title}' url='{page.url}'")

        shot = LOG_DIR / "panel_loaded.png"
        try:
            page.screenshot(path=str(shot), full_page=False)
            logging.info(f"Screenshot salvo: {shot}")
        except Exception as e:
            logging.warning(f"Falha ao fazer screenshot do painel: {e}")

        # Aqui você pode inserir suas automações (cliques/inputs etc.)
        logging.info("Runner pronto para receber comandos de automação.")
        input("Pressione ENTER para encerrar o app...")

    finally:
        try:
            if context:
                context.close()
        except Exception:
            pass
        logging.info("=== Fim do app.py ===")

if __name__ == "__main__":
    main()
