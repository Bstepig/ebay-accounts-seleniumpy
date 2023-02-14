import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


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
    wait(min_delay, max_delay)
    actions.perform()

def fill_input(driver: WebDriver, value: str, by: By, search: str, timeout=15, min_delay=0.1, max_delay=1.5):
    input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, search)))
    actions = ActionChains(driver)
    actions.move_to_element(input)
    actions.click()
    send_keys_delay_random(actions, input, value)
    wait(min_delay, max_delay)
    actions.perform()


def find_common_start_substr(str1, str2):
    shift = 0
    le = len(str1)
    while str1[:le] != str2[:le]:
        le -= 1
        shift += 1
    return shift


def fill_input_precise(driver: WebDriver, value: str, by: By, search: str, timeout=15, min_delay=0.1, max_delay=1.5):
    input: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, search)))
    actions = ActionChains(driver)
    actions.move_to_element(input)
    actions.click()
    current_value: str = input.get_attribute('value')
    shift = find_common_start_substr(current_value, value)
    add_value = value[len(current_value)-shift-1:]
    send_keys_delay_random(actions, input, [Keys.END] + [Keys.BACKSPACE] * shift)
    send_keys_delay_random(actions, input, add_value)
    wait(min_delay, max_delay)
    actions.perform()
    

def send_keys_delay_random(actions, controller, keys, min_delay=0.05, max_delay=0.25):
    for key in keys:
        controller.send_keys(key)
        wait(min_delay, max_delay)


def wait(min_delay=1, max_delay=None):
    if max_delay is None:
        time.sleep(min_delay)
    else:
        time.sleep(random.uniform(min_delay, max_delay))