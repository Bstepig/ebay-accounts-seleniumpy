import random
from typing import Dict

import undetected_chromedriver.v2 as uc
from random_user_agent.params import OperatingSystem, SoftwareName
from random_user_agent.user_agent import UserAgent

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

SOCKS = False
HEADLESS = False

RANDOM_USER_SYSTEM = 'LINUX'

LINUX_USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
]

LINUX_FIREFOX_USER_AGENTS = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
]

ANDROID_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL Build/PPP4.180612.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F27E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Pixel 2 Build/OPM2.171019.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Moto G6 Play Build/PPWS29.93-67-3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-J727P Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-J400F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Pixel XL Build/OPM2.171019.016.C1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G935U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
]

def get_browser_fingerprint(profile_dir: str, proxy=None):
    options = uc.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-auto-login")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-xss-auditor")
    options.add_argument("--ignore-certificate-errors")
    if HEADLESS:
        options.headless = True
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--remote-debugging-address=0.0.0.0")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument(f"--proxy-server={get_proxy(proxy)}")
    options.add_argument(f"--user-agent={get_random_user_agent()}")
    
    options.add_argument("--lang=de")

    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profile-shortcut-manager')

    options.add_argument(f'--user-data-dir={profile_dir}')

    if RANDOM_USER_SYSTEM == 'Android':
        options.enable_mobile()

        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}

        options.add_experimental_option(
            "mobileEmulation", mobile_emulation)
    
    browser = uc.Chrome(ChromeDriverManager().install(), options=options)
    browser.execute_script("Date.prototype.toLocaleString = function() { return new Date(this + 3600000*(new Date().getTimezoneOffset()/60 + 1)).toLocaleString(); }")
    return browser

def get_random_user_agent():
    if RANDOM_USER_SYSTEM == 'Linux':
        user_agents = LINUX_USER_AGENTS
        return random.choice(user_agents)
    
    if RANDOM_USER_SYSTEM == 'Linux Firefox':
        user_agents = LINUX_FIREFOX_USER_AGENTS
        return random.choice(user_agents)
    
    if RANDOM_USER_SYSTEM == 'Android':
        user_agents = ANDROID_USER_AGENTS
        return random.choice(user_agents)
    
    if RANDOM_USER_SYSTEM == 'Any' or True:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]

        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=1)
        return user_agent_rotator.get_random_user_agent()


def get_proxy(proxy=None):
    if SOCKS:
        return f'socks5://{proxy}'
    return f'http://{proxy}'
