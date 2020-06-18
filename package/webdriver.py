#!/usr/bin/env python3
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


def get_chrome_driver_filename():
    # get system
    system = platform.system()

    # select correct driver file
    if system == "Darwin":
        return "chromedriver_osx"
    elif system == "Linux":
        return "chromedriver_linux"

    raise RuntimeError("System must be Darwin (Mac OS) or Linux.")


def get_geckodriver_filename():
    # get system
    system = platform.system()

    # select correct driver file
    if system == "Darwin":
        return "geckodriver_osx"
    elif system == "Linux":
        return "geckodriver_linux"

    raise RuntimeError("System must be Darwin (Mac OS) or Linux.")


def get_driver(chrome=False, remote=False):
    if chrome:
        chrome_options = Options()
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--whitelisted-ips=")

        if remote:
            return webdriver.Remote(command_executor='http://chrome:4444/wd/hub',
                                    desired_capabilities= chrome_options.to_capabilities())

        filename = get_chrome_driver_filename()

        return webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), "../", filename), chrome_options=chrome_options)

    if remote:
        return webdriver.Remote(command_executor='http://firefox:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.FIREFOX)

    # get webdriver path
    filename = get_geckodriver_filename()

    return webdriver.Firefox(executable_path=os.path.join(os.path.dirname(__file__), '../', filename))
