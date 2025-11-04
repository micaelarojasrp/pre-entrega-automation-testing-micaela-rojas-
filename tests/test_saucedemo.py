import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login(driver):
    """Automatiza el login y valida redirección a /inventory.html y presencia del título 'Products'"""
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 5).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url
    assert "Swag Labs" in driver.title


def test_inventario(driver):
    """Verifica que el título y los productos estén presentes en la página de inventario"""
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert titulo == "Products"

    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0


def test_carrito(driver):
    """Agrega un producto al carrito y verifica que aparezca correctamente"""
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    driver.find_element(By.CSS_SELECTOR, ".btn_inventory").click()

    contador = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert contador == "1"

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
    producto_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert producto_en_carrito != ""
