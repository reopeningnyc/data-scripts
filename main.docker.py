from package import hospitalizations_and_deaths, testing, regional_dashboard_data, try_fetch
from selenium.common.exceptions import SessionNotCreatedException
from time import sleep


def run():
    hospitalizations_and_deaths.update_data(True)
    # regional_dashboard_data.update_data(True)
    testing.update_data()


if __name__ == "__main__":
    print("Starting data fetch...\n")
    try_fetch.wait(10, 10, 1, 2)
    run()
    print("Data fetch complete!")
