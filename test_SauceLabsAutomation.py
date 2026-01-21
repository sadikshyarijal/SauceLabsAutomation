import time
import allure
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.step("Click on element with xpath: {xpath}")
def click_element(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    assert element.is_displayed(), f"Element {xpath} not visible"
    element.click()


@allure.step("Send keys '{keys}' to element with xpath: {xpath}")
def send_keys_to_element(driver, xpath, keys):
    element = driver.find_element(By.XPATH, xpath)
    assert element.is_enabled(), f"Element {xpath} not enabled"
    element.clear()
    element.send_keys(keys)


@allure.step("Assert element exists with xpath: {xpath}")
def assert_element_exists(driver, xpath, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element = driver.find_element(By.XPATH, xpath)
    assert element.is_displayed()


@allure.title("Sauce Demo Product Search Test")
@allure.description("Search product and validate product page using Allure")
def test_sauce_demo():

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
#for headless and jenkins
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    with allure.step("Open Sauce Demo website"):
        driver.get("https://sauce-demo.myshopify.com")

    send_keys_to_element(driver, "//input[@id='search-field']", "Grey Jacket")
    time.sleep(2)

    click_element(driver, "//a[@id='product-1']")
    time.sleep(2)

    assert_element_exists(driver, "//input[@id='add']")

    driver.quit()
