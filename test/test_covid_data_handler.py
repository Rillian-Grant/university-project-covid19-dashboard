"""
Test covid_data_handler.py
"""
import unittest
import time
from urllib.request import urlopen
from dashboard.covid_data_handler import parse_csv_data, process_covid_csv_data, covid_api_request

class TestParseCsvData(unittest.TestCase):
    def test_correct_number_of_lines(self):
        self.assertEqual(len(parse_csv_data("test/data/nation_2021-10-28.csv")), 639)

class TestProcessCsvCovidData(unittest.TestCase):
    def test_correct_values(self):
        last7days_cases , current_hospital_cases , total_deaths = process_covid_csv_data(parse_csv_data("test/data/nation_2021-10-28.csv"))
        self.assertEqual(last7days_cases, 240_299)
        self.assertEqual(current_hospital_cases, 7_019)
        self.assertEqual(total_deaths, 141_544)

class TestCovidApiRequest(unittest.TestCase):
    def test_api_working(self):
        with urlopen('https://api.coronavirus.data.gov.uk/generic/healthcheck') as response:
            self.assertEqual(response.getcode(), 200)

    def test_something(self):
        covid_api_request()
        

if __name__ == '__main__':
    unittest.main()