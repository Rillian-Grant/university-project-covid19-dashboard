"""
Load and process covid data
"""

from typing import List, Tuple
from uk_covid19 import Cov19API
import sched, time, threading
import tempfile

covid_API_request_cache = {}

def parse_csv_data(csv_filename: str) -> List[str]:
    """
    :param csv_filename: Name of the file to read
    :type csv_filename: str
    :return: List of strings for each line in the file
    :rtype: List[str]
    """
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        data: List[str] = [line.strip() for line in csv_file] # TODO Not readable

    return data

def process_covid_csv_data(row_list: List[str]) -> Tuple[int, int, int]:
    """
    :param row_list: List of rows from an appropriately formatted csv file
    :type row_list: List[str]
    :return: Cases in the last 7 days, the current number of hospitalized cases and the cumulative number of deaths
    :rtype: Tuple[int, int, int]
    """
    # Split each row in the list into a list of the values that were comma separated
    data = list(map(lambda row: row.split(","), row_list))

    # The first row contains the headers. The second row is empty and the third has incomplete data
    data_from_last_7_days = data[3:10]
    data_from_last_7_days = list(map(lambda column: column[6], data_from_last_7_days))
    data_from_last_7_days = list(map(int, data_from_last_7_days))
    cases_in_last_7_days = sum(data_from_last_7_days)

    current_hospital_cases = int(data[1][5])

    for row in data[1:]:
        if row[4] != "":
            total_deaths = int(row[4])
            break
 
    return (cases_in_last_7_days, current_hospital_cases, total_deaths)

def covid_API_request(location: str="Exeter", location_type: str="ltla"):
    api = Cov19API(
        filters=[
            "areaType=" + location_type,
            "areaName=" + location
        ],
        structure={ # TODO https://coronavirus.data.gov.uk/details/developers-guide/main-api#structure-metrics
            "date": "date",
            "newCasesByPublishDate": "newCasesByPublishDate",
            "cumCasesByPublishDate": "cumCasesByPublishDate",
            "hospitalCases": "hospitalCases",
            "newCasesBySpecimenDate": "newCasesBySpecimenDate",
            "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
            "newCasesByPublishDateRollingSum": "newCasesByPublishDateRollingSum"
        }
        
    )

    data = api.get_json()

    return data

def get_periodically_updated_covid_API_request(): return covid_API_request_cache

def schedule_covid_updates(update_interval, update_name, *args):
    def update_cached_covid_data():
        print("Here")
        data = covid_API_request(*args)
        global covid_API_request_cache
        covid_API_request_cache = data
        scheduler.enter(update_interval, 0, update_cached_covid_data)
        return data

    scheduler = sched.scheduler(time.time, time.sleep)
    update_cached_covid_data()
    thread = threading.Thread(target=scheduler.run)
    thread.daemon = True
    thread.start()




################################################################################


def dashboard_data():

    def iterate_till_key_not_none(list_of_dicts, key):
        for dict in list_of_dicts:
            if dict[key] != None: return dict[key]

    """ def find_7_day_infection_rates(data):
        week_infection_rate=0
        days_done=0
        data_index=0
        while days_done < 7:
            num = data["data"][1:][data_index][""]
            if num != None:
                week_infection_rate += num
                days_done+=1
            data_index+=1
        return week_infection_rate """


    local_data = covid_API_request()
    national_data = covid_API_request(location="England", location_type="nation")

    sorted = {
        "deaths_total": iterate_till_key_not_none(national_data["data"], "cumDeaths28DaysByDeathDate"),
        "hospital_cases": iterate_till_key_not_none(national_data["data"], "hospitalCases"),
        "local_7day_infections": iterate_till_key_not_none(local_data["data"], "newCasesByPublishDateRollingSum"),
        "national_7day_infections": iterate_till_key_not_none(national_data["data"], "newCasesByPublishDateRollingSum")
    }

    return sorted