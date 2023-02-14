from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from tools.config import COUNTRY_NUMBER_CODE, EBAY_COUNTRY_CODE
from tools.phone_verification import get_activation, get_number
from tools.shortcuts import click_element, fill_input


def ebay_phone_verification(driver: WebDriver):
    select_el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'phone-verification-country')))
    select = Select(select_el)
    select.select_by_visible_text(EBAY_COUNTRY_CODE)
    res = get_number()
    number = str(res.get('number'))
    number_tail = number[len(COUNTRY_NUMBER_CODE):]

    fill_input(driver, number_tail, By.ID, 'phone-verification-number')
    click_element(driver, By.XPATH,
                  '//footer /button[@class="Button-primary"]')

    code = get_activation(res['id'])
    fill_input(driver, code, By.ID, 'phone-verification-code')
    click_element(driver, By.XPATH,
                  '//footer /button[@class="Button-primary"]')
