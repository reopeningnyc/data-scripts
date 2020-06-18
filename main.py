from package import new_hospitalizations_and_deaths, regional_dashboard_data, testing, total_hospitalizations

if __name__ == "__main__":
    new_hospitalizations_and_deaths.update_data()
    testing.update_data()
    regional_dashboard_data.update_data(
        "hospital-bed-vacancies", "Total Hospital Beds"
    )
    regional_dashboard_data.update_data(
        "icu-bed-availability", "ICU Beds"
    )
    total_hospitalizations.update_data()
