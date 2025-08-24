# login_once.py
# -----------------------------------------------------------
# Cria e usa um PERFIL NÃO-PADRÃO do Chrome (clonando itens essenciais
# do seu "Default"), abre o Chrome oficial com extensões/certificados,
# navega ao PJe para login manual e salva a sessão em state.json.
# Gera logs/trace/screenshots em ./logs.
# -----------------------------------------------------------

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
from pathlib import Path
import sys
import time
import logging
import traceback
import os
import shutil
import sqlite3

# ===================== CONFIG =====================
# Perfil ORIGEM (padrão) - de onde lemos as preferências/extensões:
SRC_USER_DATA_DIR = r"C:\Users\mario\AppData\Local\Google\Chrome\User Data"  # RAIZ (contém "Default")
SRC_PROFILE_NAME  = "Default"                                                # "Default" ou "Profile 1", ...

# Perfil de AUTOMAÇÃO (não-padrão) - destino:
DST_USER_DATA_DIR = str(Path(os.getenv("LOCALAPPDATA", r"C:\Users\mario\AppData\Local")) / "ChromeAutomation" / "User Data")
DST_PROFILE_NAME  = "Default"  # manter "Default" dentro do novo root

# URLs PJe
LOGIN_URL       = "https://pje.tjdft.jus.br/pje/"
TARGET_URL      = "https://pje.tjdft.jus.br/pje/ng2/dev.seam#/painel-usuario-interno"
PANEL_SELECTOR  = None          # opcional: ex. "app-painel-usuario-interno"

# Tempo e artefatos
TIMEOUT_SEC     = 300           # 5 min
STATE_FILE      = "state.json"
LOG_DIR         = Path("logs")
LOG_FILE        = LOG_DIR / "login.log"
TRACE_FILE      = LOG_DIR / "trace.zip"

# (opcional) binário do Chrome; se vazio, usa channel="chrome"
CHROME_PATH     = ""  # ex.: r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# ==================================================


# ---------------- LOGGING ----------------
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
    console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
    logging.getLogger().addHandler(console)
    logging.info("=== Início do login_once ===")
    logging.info(f"Perfil origem: {SRC_USER_DATA_DIR} -> {SRC_PROFILE_NAME}")
    logging.info(f"Perfil automação (destino): {DST_USER_DATA_DIR} -> {DST_PROFILE_NAME}")


# ---------------- UTIL ----------------
def kill_chrome_processes():
    """Fecha processos que seguram locks no perfil (ignora erros)."""
    cmds = [
        r'taskkill /IM chrome.exe /F',
        r'taskkill /IM GoogleCrashHandler.exe /F',
        r'taskkill /IM GoogleCrashHandler64.exe /F',
        r'taskkill /IM chrome_proxy.exe /F',
    ]
    for cmd in cmds:
        try:
            os.system(cmd + " >NUL 2>&1")
        except Exception:
            pass


def safe_copy_file(src: Path, dst: Path):
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        logging.info(f"[COPY] {src.name} -> OK")
        return True
    except Exception as e:
        logging.warning(f"[COPY] Falha ao copiar {src}: {e}")
        return False


def is_sqlite_unlocked(db_path: Path) -> bool:
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        conn.close()
        return True
    except Exception:
        return False


def copy_essential_profile():
    """
    Copia apenas o essencial do perfil 'Default' para o destino:
      - Arquivos: Preferences, Secure Preferences, Cookies*, Login Data*, Web Data*, History*
      - Pasta: Extensions/ (com filtros leves)
      - Arquivo raiz: 'Local State'
    Se algum banco SQLite estiver bloqueado, ignora sem falhar.
    """
    src_root = Path(SRC_USER_DATA_DIR)
    dst_root = Path(DST_USER_DATA_DIR)
    src = src_root / SRC_PROFILE_NAME
    dst = dst_root / DST_PROFILE_NAME

    if not src_root.exists() or not src.exists():
        logging.error(f"Origem não encontrada: {src}")
        # Ainda assim, cria destino vazio para Chrome inicializar
        dst.mkdir(parents=True, exist_ok=True)
        return False

    # Cria destino
    dst.mkdir(parents=True, exist_ok=True)

    # 1) 'Local State' (na raiz do User Data)
    safe_copy_file(src_root / "Local State", dst_root / "Local State")

    # 2) Preferências (JSONs)
    safe_copy_file(src / "Preferences", dst / "Preferences")
    safe_copy_file(src / "Secure Preferences", dst / "Secure Preferences")

    # 3) Bancos SQLite (se não estiverem bloqueados)
    for sqlite_name in ["Cookies", "Cookies-journal", "Login Data", "Login Data For Account", "Web Data", "History"]:
        s = src / sqlite_name
        if s.exists():
            if is_sqlite_unlocked(s):
                safe_copy_file(s, dst / sqlite_name)
            else:
                logging.warning(f"[LOCK] {sqlite_name} parece bloqueado. Ignorando.")

    # 4) Extensões
    ext_src = src / "Extensions"
    ext_dst = dst / "Extensions"
    if ext_src.exists():
        try:
            if ext_dst.exists():
                shutil.rmtree(ext_dst, ignore_errors=True)
            shutil.copytree(ext_src, ext_dst, ignore=lambda d, names: ["_metadata"] if "_metadata" in names else [])
            logging.info("[COPY] Extensions/ -> OK")
        except Exception as e:
            logging.warning(f"[COPY] Falha ao copiar Extensions/: {e}")
    else:
        logging.info("Sem pasta Extensions/ na origem (ok).")

    return True


# ---------------- STEALTH ----------------
STEALTH_JS = r"""
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
window.chrome = { runtime: {} };
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
  parameters && parameters.name === 'notifications'
    ? Promise.resolve({ state: 'prompt' })
    : originalQuery(parameters)
);
"""


# ---------------- WAITERS & NAV ----------------
def wait_until_logged(page):
    logging.info("Aguardando conclusão do login no PJe...")
    start = time.time()
    last_url = ""

    while True:
        elapsed = time.time() - start
        try:
            cur = page.url or ""
        except Exception:
            cur = ""

        if cur != last_url:
            logging.info(f"URL atual: {cur}")
            last_url = cur

        # Critério 1: URL do painel
        if TARGET_URL.split("#")[0] in cur.split("#")[0]:
            logging.info("Painel detectado pela URL.")
            return

        # Critério 2: seletor característico (se fornecido)
        if PANEL_SELECTOR:
            try:
                page.wait_for_selector(PANEL_SELECTOR, timeout=1000)
                logging.info(f"Painel detectado pelo seletor: {PANEL_SELECTOR}")
                return
            except PWTimeoutError:
                pass

        if elapsed > TIMEOUT_SEC:
            logging.warning("Tempo limite atingido aguardando login.")
            try:
                input("Pressione ENTER aqui para salvar o estado atual mesmo assim...")
            except KeyboardInterrupt:
                pass
            return

        time.sleep(1)


def safe_goto(page, url: str, note: str, attempts: int = 3):
    for i in range(1, attempts + 1):
        try:
            logging.info(f"[NAV {i}/{attempts}] {note}: {url}")
            page.goto(url, wait_until="load", timeout=45000)
            logging.info("[NAV] OK")
            return True
        except Exception as e:
            logging.warning(f"[NAV] Falha ({i}/{attempts}): {e}")
            screenshot = LOG_DIR / f"nav_fail_{int(time.time())}.png"
            try:
                page.screenshot(path=str(screenshot))
                logging.info(f"[NAV] Screenshot salvo: {screenshot}")
            except Exception as se:
                logging.warning(f"[NAV] Falha ao tirar screenshot: {se}")
            time.sleep(2)
    return False


# ---------------- MAIN ----------------
def main():
    setup_logging()

    # Fecha processos e prepara perfil de automação (cópia essencial)
    logging.info("Fechando processos do Chrome para liberar arquivos...")
    kill_chrome_processes()
    ok_copy = copy_essential_profile()
    if ok_copy:
        logging.info("Cópia essencial concluída.")
    else:
        logging.info("Seguindo com perfil de automação (pode estar vazio).")

    logging.info("Abrindo Chrome com perfil de automação (não-padrão), extensões (se copiadas) e sem flags problemáticas...")

    with sync_playwright() as p:
        launch_kwargs = dict(
            user_data_dir=str(DST_USER_DATA_DIR),  # RAIZ do perfil de automação
            headless=False,
            args=[
                "--start-maximized",
                f"--profile-directory={DST_PROFILE_NAME}",  # normalmente "Default" dentro do novo root
                "--no-first-run",
                "--no-default-browser-check",
            ],
            # Mantém extensões e remove a faixa de automação padrão
            ignore_default_args=[
                "--enable-automation",
                "--disable-extensions",
                "--no-sandbox",  # evita banner "linha de comando não suportada"
            ],
            locale="pt-BR",
            accept_downloads=True,
        )

        context = None
        try:
            if CHROME_PATH:
                context = p.chromium.launch_persistent_context(executable_path=CHROME_PATH, **launch_kwargs)
            else:
                context = p.chromium.launch_persistent_context(channel="chrome", **launch_kwargs)

            context.add_init_script(STEALTH_JS)

            # Trace
            try:
                LOG_DIR.mkdir(exist_ok=True)
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
            except Exception as te:
                logging.warning(f"Tracing não pôde iniciar: {te}")

            # ======= ABA INICIAL: NÃO criar nova aba; usar a existente =======
            page = None
            # 1) Se já existe alguma aba, usa a primeira visível
            if context.pages:
                page = context.pages[0]
                logging.info(f"[PAGE] Reutilizando aba existente: {page.url}")
            # 2) Senão, aguarda surgir uma aba (até 10s)
            if page is None:
                try:
                    logging.info("[PAGE] Aguardando primeira aba surgir...")
                    page = context.wait_for_event("page", timeout=10000)
                    logging.info(f"[PAGE] Primeira aba detectada: {getattr(page, 'url', 'desconhecida')}")
                except Exception as e:
                    logging.warning(f"[PAGE] Nenhuma aba apareceu: {e}")
            # 3) Se ainda não temos página, última tentativa: criar nova
            if page is None:
                try:
                    logging.info("[PAGE] Tentando criar nova aba como fallback...")
                    page = context.new_page()
                    logging.info("[PAGE] Nova aba criada com sucesso.")
                except Exception as e:
                    logging.error(f"[PAGE] Falha ao criar nova aba: {e}")
                    raise

            try:
                page.bring_to_front()
            except Exception:
                pass

            # Handlers de diagnóstico
            page.on("console", lambda msg: logging.info(f"[CONSOLE] {msg.type().upper()}: {msg.text()}"))
            page.on("pageerror", lambda exc: logging.error(f"[PAGEERROR] {exc}"))
            page.on("requestfailed", lambda req: logging.error(f"[REQFAILED] {req.url} -> {req.failure.error_text if req.failure else ''}"))
            page.on("response", lambda resp: (
                logging.info(f"[HTTP {resp.status}] {resp.url}") if "pje.tjdft.jus.br" in resp.url else None
            ))

            # Navegações
            if not safe_goto(page, LOGIN_URL, "Abrindo página inicial do PJe"):
                logging.error("Falha ao abrir a página inicial do PJe. Abortando.")
                try:
                    page.screenshot(path=str(LOG_DIR / "fail_open_login.png"))
                except Exception:
                    pass
                return

            safe_goto(page, TARGET_URL, "Tentando acessar painel (o PJe redireciona para login se necessário)")

            wait_until_logged(page)

            logging.info(f"Salvando sessão em {STATE_FILE} ...")
            context.storage_state(path=STATE_FILE)
            logging.info("Sessão salva com sucesso.")

        except Exception as e:
            logging.error("Exceção não tratada durante a execução.")
            logging.error(str(e))
            logging.error(traceback.format_exc())
            try:
                if context and context.pages:
                    context.pages[-1].screenshot(path=str(LOG_DIR / "fatal_error.png"))
                    logging.info(f"Screenshot salvo: {LOG_DIR / 'fatal_error.png'}")
            except Exception:
                pass
        finally:
            try:
                if context:
                    context.tracing.stop(path=str(TRACE_FILE))
                    logging.info(f"Trace salvo em: {TRACE_FILE}")
            except Exception as te:
                logging.warning(f"Falha ao salvar trace: {te}")
            try:
                if context:
                    context.close()
            except Exception:
                pass

    logging.info("=== Fim do login_once ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Encerrado pelo usuário.")
        sys.exit(1)
