import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


REPO_ROOT = os.path.dirname(__file__)
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def chrome_options():
opts = Options()
# Opciones útiles (podés quitar headless si querés ver el navegador)
# opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
return opts


@pytest.fixture(scope="function")
def driver(chrome_options, request):
"""Fixture que crea y destruye el WebDriver por test (tests independientes)."""
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)


yield driver


# teardown: en caso de fallo guardar captura (otra defensa)
try:
# se salva siempre al final por si el test dejó el navegador en un estado raro
pass
finally:
driver.quit()


# Hook para tomar screenshot automáticamente en fallos y adjuntar ruta al reporte
def pytest_runtest_makereport(item, call):
"""Hook para capturar pantallas si un test falla."""
if call.when == "call":
outcome = call.excinfo
if outcome is not None:
driver_fixture = item.funcargs.get('driver')
if driver_fixture:
screenshot_name = f"{item.name}.png"
path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
try:
driver_fixture.save_screenshot(path)
# adhiere la ruta a node para que otros hooks lo lean o el usuario lo use
if not hasattr(item, 'extra'): item.extra = {}
item.extra['screenshot'] = path
except Exception:
pass
