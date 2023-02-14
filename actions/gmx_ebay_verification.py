from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from tools.shortcuts import click_element, fill_input, switch_to, wait
from tools.user import Profile


def gmx_ebay_verification(driver: WebDriver, profile: Profile, page: str):
    driver.get(page)

    try:
        wait(10)
        driver.switch_to.frame("thirdPartyFrame_permission_dialog")
        driver.switch_to.frame("permission-iframe")
        click_element(driver, By.XPATH,
                        '//button[@data-goto-view="CompletionView"]')

    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()

    try:
        wait(10)
        driver.switch_to.frame("thirdPartyFrame_permission_dialog")
        driver.switch_to.frame("permission-iframe")
        click_element(driver, By.ID, 'close-layer')
    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()

    try:
        wait(3)
        driver.switch_to.frame("thirdPartyFrame_permission_dialog")
        driver.switch_to.frame("permission-iframe")
        click_element(driver, By.CLASS_NAME,
                        'layer-apply lux-button lux-button--tertiary-ghost')
    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()

    try:
        el = driver.find_element(
            By.XPATH, '//div[@data-notification-type="error-light"]')
        if el:
            form = driver.find_element(By.ID, 'freemailLoginForm')
            fill_input(driver, profile.get_email(),
                        By.ID, 'freemailLoginUsername')
            fill_input(driver, profile.email_password,
                        By.ID, 'freemailLoginPassword')
            click_element(form, By.TAG_NAME, 'button')
    except:
        pass

    switch_to(driver, By.ID, 'thirdPartyFrame_home')
    click_element(driver, By.XPATH,
                    '//span[@class="address" contains(text(), "eBay")]')
    driver.switch_to.default_content()

    switch_to(driver, By.ID, 'thirdPartyFrame_mail')
    switch_to(driver, By.ID, 'mail-detail')
    click_element(driver, By.TAG_NAME, 'a')