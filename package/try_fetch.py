from requests import get
from requests.exceptions import ConnectionError
from time import sleep
from selenium.common.exceptions import SessionNotCreatedException
from urllib3.exceptions import MaxRetryError


def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk))


def wait(tries, initial_delay, delay, backoff):
    sleep(initial_delay)
    active_delay = delay

    for n in range(tries):
        try:
            resp = get('http://localhost:4444/wd/hub/status')
            ready = resp.json()['value']['ready']

            if ready:
                return True

        except ConnectionError as err:
            prRed("ERROR: %s" % err)

        prYellow("Firefox not yet ready. Retrying in %s seconds...\n" % active_delay)
        sleep(active_delay)
        active_delay *= backoff

    raise RuntimeError("Failed to run tests after %s tries.\n" % tries)
