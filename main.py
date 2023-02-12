import pathlib
from threading import Thread

from actions.ebay_phone import ebay_phone_verification
from actions.gmx_ebay_verification import gmx_ebay_verification
from actions.register_ebay import register_ebay
from actions.register_gmx import register_gmx
from tools.driver import get_browser_fingerprint
from tools.piaproxy import load_pia_proxy
from tools.store import store_result
from tools.user import Profile

path = pathlib.Path().resolve()


def register_account(port):

    proxy_res = load_pia_proxy(port)

    profile = Profile(proxy_res)
    profile_dir = f'{path}/profiles/{profile.get_email()}'

    driver = get_browser_fingerprint(profile_dir, proxy_res['proxy'])

    gmx_last_url = register_gmx(driver)
    register_ebay(driver, profile)
    gmx_ebay_verification(driver, profile, gmx_last_url)
    ebay_phone_verification(driver)
    store_result(proxy_res, profile_dir, profile)

    # driver.get('https://bot.sannysoft.com')
    # driver.get("https://nowsecure.nl")

    driver.close()
    driver.quit()


start_port = 40000
number_of_threads = 1

threads = []

for port_tail in range(number_of_threads):
    port = str(start_port + port_tail)
    t = Thread(target=register_account, args=[port])
    t.start()
    threads.append(t)

for t in threads:
    t.join()
