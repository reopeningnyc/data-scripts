#!/usr/bin/env python3
import os
import platform


def get_geckodriver_filename():
    # get system
    system = platform.system()

    print(system)

    # select correct driver file
    if system == "Darwin":
        return "geckodriver_osx"
    elif system == "Linux":
        return "geckodriver_linux"

    raise RuntimeError("System must be Darwin (Mac OS) or Linux.")


def get_geckodriver_path() -> str:
    filename = get_geckodriver_filename()

    return os.path.join(os.path.dirname(__file__), '../', filename)
