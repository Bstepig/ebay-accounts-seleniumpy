import pathlib
import random
from threading import Thread
import time

from captchas import get_captcha_solve, solve_captcha, solve_recaptcha
from driver import get_browser_fingerprint
from user import Profile
from keys import COUNTRY_NUMBER_CODE, EBAY_COUNTRY_CODE
from phone_verification import get_number, get_activation
from piaproxy import load_pia_proxy

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

import undetected_chromedriver.v2 as uc
import time

path = pathlib.Path().resolve()


def reg(port):

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

    def inputGmx(driver: WebDriver, inputDataTest: str, value: str):
        fill_input(driver, value, By.XPATH,
                   "//input[@data-test=\"" + inputDataTest + "\"]")

    def tryToClose(driver: WebDriver):
        try:
            time.sleep(5)
            switch_to(driver, By.NAME, 'landingpage')

            driver.switch_to.frame(0)
            click_element(driver, By.ID, 'save-all-pur')

            time.sleep(5)

        except Exception as e:
            print(e)

            pass
        finally:
            driver.switch_to.default_content()

    def register_ebay():

        driver.get('https://www.ebay-kleinanzeigen.de/')

        acceptBanner = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'gdpr-banner-accept')))
        acceptBanner.click()
        time.sleep(3)
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

        solve_token = get_captcha_solve(recaptcha_request_id)
        driver.execute_script(
            f"document.getElementById('g-recaptcha-response').innerHTML = '{solve_token}'")

        submitButton = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'registration-submit')))
        submitButton.click()

    def register_gmx():
        driver.get('https://gmx.net')

        tryToClose(driver)

        click_element(driver, By.XPATH,
                      '//a[@data-importance="ghost"]', timeout=30)

        driver.switch_to.default_content()

        click_element(driver, By.XPATH, '//a[@class="key l button"]')

        while True:
            inputGmx(driver, "check-email-availability-email-input",
                     profile.get_email_name())
            click_element(
                driver, By.XPATH, '//button[@data-test="check-email-availability-check-button"]')

            def find_email_checking_result(driver: WebDriver):
                try:
                    el = driver.find_element(
                        By.XPATH, '//div[@data-test="check-email-availability-success-message"]')
                    if el:
                        return 2  # Success
                except:
                    pass

                try:
                    el = driver.find_element(
                        By.XPATH, '//onereg-error-messages[@data-test="check-email-availability-failure-message"]')
                    if el:
                        return 1  # Failure
                except:
                    pass

            result = WebDriverWait(driver, 60).until(
                find_email_checking_result)

            if result == 1:
                profile.next_email_name()
                pass

            if result == 2:
                break

        click_element(driver, By.XPATH,
                      f'//onereg-radio-wrapper[{str(profile.genderIndex)}]')

        inputGmx(driver, "first-name-input", profile.firstName)
        inputGmx(driver, "last-name-input", profile.lastName)

        inputGmx(driver, "postal-code-input", profile.postalCode)
        inputGmx(driver, "town-input", profile.town)
        inputGmx(driver, "street-and-number-input",
                 profile.street + ", " + profile.home)

        inputGmx(driver, "day", str(profile.birthDay))
        inputGmx(driver, "month", str(profile.birthMonth))
        inputGmx(driver, "year", str(profile.birthYear))

        inputGmx(driver, "choose-password-input", profile.email_password)
        inputGmx(driver, "choose-password-confirm-input",
                 profile.email_password)

        inputGmx(driver, "mobile-phone-input", profile.email_phone)

        captcha_img_el = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'captchaImage')))
        captcha_base64 = captcha_img_el.get_attribute('src')
        captcha_request_id = solve_captcha(captcha_base64)
        captcha_code = get_captcha_solve(captcha_request_id)
        inputGmx(driver, "captcha-input", captcha_code)

        click_element(driver, By.XPATH,
                      '//button[@data-test="create-mailbox-create-button"]')

        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//h1[contains(text(), "Mobilfunknummer verifizieren")]')))

            return False
        except TimeoutException:

            pass

        def find_email_ending():
            try:
                el = driver.find_element(By.ID, 'continueButton')
                if el:
                    return 2  # Success
            except:
                pass

            try:
                el = driver.find_element(
                    By.XPATH, '//h1[contains(text(), "Mobilfunknummer verifizieren")]')
                if el:
                    return 1  # Failure: Phone Verification
            except:
                pass

        email_result = WebDriverWait(driver, 60).until(find_email_ending)

        if email_result == 1:
            return False
        if email_result == 2:
            pass

        try:
            time.sleep(5)
            driver.switch_to.frame("thirdPartyFrame_layer")
            click_element(driver, By.CLASS_NAME, 'button large secondary')
        except Exception as e:
            print(e)
            pass
        finally:
            driver.switch_to.default_content()

        return driver.current_url

    def gmx_ebay_verification(page: str):
        driver.get(page)

        try:

            time.sleep(10)
            driver.switch_to.frame("thirdPartyFrame_permission_dialog")
            driver.switch_to.frame("permission-iframe")
            click_element(driver, By.XPATH,
                          '//button[@data-goto-view="CompletionView"]')

        except Exception as e:
            print(e)
            pass
        finally:
            driver.switch_to.default_content()

        try:
            time.sleep(10)
            driver.switch_to.frame("thirdPartyFrame_permission_dialog")
            driver.switch_to.frame("permission-iframe")
            click_element(driver, By.ID, 'close-layer')
        except Exception as e:
            print(e)
            pass
        finally:
            driver.switch_to.default_content()

        try:
            time.sleep(3)
            driver.switch_to.frame("thirdPartyFrame_permission_dialog")
            driver.switch_to.frame("permission-iframe")
            click_element(driver, By.CLASS_NAME,
                          'layer-apply lux-button lux-button--tertiary-ghost')
        except Exception as e:
            print(e)
            pass
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

    def ebay_phone_verification():
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

    def store_result():
        results = []
        results.append(f'Proxy: {proxy_res["proxy"]}')
        results.append(f'Proxy IP: {proxy_res["out_ip"]}')
        results.append(f'Proxy City: {proxy_res["city"]}')
        results.append(f'Email: {profile.get_email()}')
        results.append(f'Email Password: {profile.email_password}')
        results.append(f'eBay Password: {profile.ebay_password}')

        file = open(profile_dir + '/result.txt', 'w')
        file.writelines(results)
        file.close()
        print('\033[92m' + f"Success! {profile.get_email()}" + '\033[0m')

    proxy_res = load_pia_proxy(port)

    profile = Profile(proxy_res)
    profile_dir = f'{path}/profiles/{profile.get_email()}'

    driver = get_browser_fingerprint(profile_dir, proxy_res['proxy'])

    gmx_last_url = register_gmx()
    register_ebay()
    gmx_ebay_verification(gmx_last_url)
    ebay_phone_verification()
    store_result(profile)
    

    # driver.get('https://bot.sannysoft.com')
    # driver.get("https://nowsecure.nl")

    driver.close()
    driver.quit()


start_port = 40000
number_of_threads = 1

threads = []

for port_tail in range(number_of_threads):
    port = str(start_port + port_tail)
    t = Thread(target=reg, args=[port])
    t.start()
    threads.append(t)

for t in threads:
    t.join()
