from package import total_hospitalizations, try_fetch
from time import sleep


def run():
    total_hospitalizations.update_data(True)


if __name__ == "__main__":
    print("Starting data fetch...\n")
    try_fetch.wait(10, 10, 1, 2)
    run()
    print("Data fetch complete!")
