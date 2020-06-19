from package import regional_dashboard_data, try_fetch
from time import sleep


def run():
    regional_dashboard_data.update_data(
        "hospital-bed-vacancies", "Total Hospital Beds", True
    )


if __name__ == "__main__":
    print("Starting data fetch...\n")
    try_fetch.wait(10, 10, 1, 2)
    run()
    print("Data fetch complete!")
