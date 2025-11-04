from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def wait_for_element(driver, by, selector, timeout=10):
return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))




def wait_for_elements(driver, by, selector, timeout=10):
return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, selector)))
