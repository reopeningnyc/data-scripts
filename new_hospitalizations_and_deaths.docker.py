from package import new_hospitalizations_and_deaths, try_fetch
from time import sleep


def run():
    new_hospitalizations_and_deaths.update_data()


if __name__ == "__main__":
    print("Starting data fetch...\n")
    try_fetch.wait(10, 10, 1, 2)
    run()
    print("Data fetch complete!")
