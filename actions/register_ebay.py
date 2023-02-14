from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tools.captchas import get_recaptcha_solve, solve_recaptcha
from tools.shortcuts import fill_input, wait
from tools.user import Profile


def register_ebay(driver: WebDriver, profile: Profile):

    driver.get('https://www.ebay-kleinanzeigen.de/')

    acceptBanner = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'gdpr-banner-accept')))
    acceptBanner.click()
    wait(3)
    startRegistration = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'button-secondary')))
    startRegistration.click()

    recaptcha = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'registration-recaptcha')))
    sitekey = recaptcha.get_attribute('data-sitekey')
    recaptcha_request_id = solve_recaptcha(sitekey, driver.current_url)

    fill_input(driver, profile.get_email(), By.ID, 'registration-email')
    fill_input(driver, profile.ebay_password,
                By.ID, 'registration-password')

    solve_token = get_recaptcha_solve(recaptcha_request_id)
    driver.execute_script(
        f"document.getElementById('g-recaptcha-response').innerHTML = '{solve_token}'")

    submitButton = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'registration-submit')))
    submitButton.click()


