import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture
def setup_driver():
    """Inicializa el WebDriver y lo cierra al finalizar cada test"""
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")

    # Espera explícita
    wait = WebDriverWait(driver, 10)

    yield driver  # proporciona el driver al test

    # teardown: se ejecuta siempre al final del test
    try:
        driver.quit()
    except Exception:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura pantalla automáticamente si el test falla"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("setup_driver")
        if driver:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_name = f"reports/screenshot_{item.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_name)
            print(f"\n🖼 Screenshot guardado: {screenshot_name}")
