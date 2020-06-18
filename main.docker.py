from package import new_hospitalizations_and_deaths, regional_dashboard_data, testing, total_hospitalizations, try_fetch
from time import sleep


def run():
    new_hospitalizations_and_deaths.update_data()
    testing.update_data()
    regional_dashboard_data.update_data(
        "hospital-bed-vacancies", "Total Hospital Beds", True
    )
    regional_dashboard_data.update_data(
        "icu-bed-availability", "ICU Beds", True
    )
    total_hospitalizations.update_data(True)


if __name__ == "__main__":
    print("Starting data fetch...\n")
    try_fetch.wait(10, 10, 1, 2)
    run()
    print("Data fetch complete!")
