import pytest
import time
from selenium.webdriver.common.by import By
from utils.selenium_helpers import wait_for_element, wait_for_elements


BASE_URL = "https://www.saucedemo.com/"


@pytest.mark.order(1)
def test_login(driver):
"""Automatiza el login y valida redirección a /inventory.html y presencia del título 'Products'"""
driver.get(BASE_URL)


# inputs identificables por id
user = wait_for_element(driver, By.ID, "user-name")
pwd = wait_for_element(driver, By.ID, "password")
login_btn = wait_for_element(driver, By.ID, "login-button")


user.send_keys("standard_user")
pwd.send_keys("secret_sauce")
login_btn.click()


# espera explícita a que la url contenga /inventory.html
WebDriverWait = __import__('selenium.webdriver.support.ui', fromlist=['WebDriverWait']).WebDriverWait
EC = __import__('selenium.webdriver.support.expected_conditions', fromlist=['expected_conditions']).expected_conditions
WebDriverWait(driver, 10).until(lambda d: "/inventory.html" in d.current_url)


# valida título visible 'Products' (selector .product_label o div .header_secondary_container)
title = wait_for_element(driver, By.CLASS_NAME, "title")
assert "Products" in title.text or "PRODUCTS" in title.text


@pytest.mark.order(2)
def test_inventory_catalogue(driver):
"""Verifica que haya productos visibles, valida título y lista nombre/precio del primero."""
driver.get(BASE_URL)


# login rápido reutilizando las acciones (podríamos extraer a helper si quisiéramos)
wait_for_element(driver, By.ID, "user-name").send_keys("standard_user")
wait_for_element(driver, By.ID, "password").send_keys("secret_sauce")
wait_for_element(driver, By.ID, "login-button").click()


WebDriverWait = __import__('selenium.webdriver.support.ui', fromlist=['WebDriverWait']).WebDriverWait
WebDriverWait(driver, 10).until(lambda d: "/inventory.html" in d.current_url)


title = wait_for_element(driver, By.CLASS_NAME, "title")
assert "Products" in title.text or "PRODUCTS" in title.text


# verificar presencia de al menos un producto
products = wait_for_elements(driver, By.CLASS_NAME, "inventory_item")
assert len(products) > 0


# listar nombre y precio del primero
first = products[0]
name = first.find_element(By.CLASS_NAME, "inventory_item_name").text
price = first.find_element(By.CLASS_NAME, "inventory_item_price").text
# Imprime para que quede en logs
print(f"Primer producto: {name} - {price}")


@pytest.mark.order(3)
def test_add_to_cart_and_verify(driver):
"""Agrega el primer producto al carrito y valida contador y que aparezca en el carrito."""
driver.get(BASE_URL)


# login
wait_for_element(driver, By.ID, "user-name").send_keys("standard_user")
wait_for_element(driver, By.ID, "password").send_keys("secret_sauce")
wait_for_element(driver, By.ID, "login-button").click()


WebDriverWait = __import__('selenium.webdriver.support.ui', fromlist=['WebDriverWait']).WebDriverWait
WebDriverWait(driver, 10).until(lambda d: "/inventory.html" in d.current_url)


# agregar primer producto (botón con clase btn_inventory)
cart_first_name = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
