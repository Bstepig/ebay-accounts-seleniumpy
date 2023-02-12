import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def switch_to(driver, by: By, value: str, timeout=30):
    iframe = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value)))
    driver.switch_to.frame(iframe)

def click_element(driver: WebDriver, by: By, search: str, timeout=15, min_delay=0.1, max_delay=1.5):
    button = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, search)))
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click()
    time.sleep(random.uniform(min_delay, max_delay))
    actions.perform()

def fill_input(driver: WebDriver, value: str, by: By, search: str, timeout=15, min_delay=0.1, max_delay=1.5):
    input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, search)))
    actions = ActionChains(driver)
    actions.move_to_element(input)
    actions.click()
    send_keys_delay_random(actions, input, value)
    time.sleep(random.uniform(min_delay, max_delay))
    actions.perform()

def send_keys_delay_random(actions, controller, keys, min_delay=0.05, max_delay=0.25):
    for key in keys:
        controller.send_keys(key)
        time.sleep(random.uniform(min_delay, max_delay))
