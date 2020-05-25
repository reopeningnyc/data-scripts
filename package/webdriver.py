#!/usr/bin/env python3
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_geckodriver_filename():
    # get system
    system = platform.system()

    # select correct driver file
    if system == "Darwin":
        return "geckodriver_osx"
    elif system == "Linux":
        return "geckodriver_linux"

    raise RuntimeError("System must be Darwin (Mac OS) or Linux.")


def get_geckodriver_path() -> str:
    filename = get_geckodriver_filename()

    return os.path.join(os.path.dirname(__file__), '../', filename)


def get_driver(remote=False):
    if remote:
        return webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.FIREFOX)

    # get webdriver path
    webdriver_path = get_geckodriver_path()

    return webdriver.Firefox(executable_path=webdriver_path)
