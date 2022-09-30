import functools
import time
import unittest
import json
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import jsonpath


class TestCompare_Data_JSON_And_UI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global driver, URL

        driver = webdriver.Chrome(ChromeDriverManager().install())

        URL = 'https://testsite.com/test'
        driver.maximize_window()
        driver.implicitly_wait(20)

    # Get data from page with Selenium Webdriver
    @classmethod
    def test_1_Snapshot_Get_Metrics_UI(cls):

        global metric1_nums, metric2_nums

        driver.get(URL)

        # Get First Metric
        metric_list = driver.find_elements(By.XPATH, '//td[@propertyname="frequencyWs1"]/div/span')
        metric1_nums = []

        for element in metric_list:
            metric1_nums.append(int(element.get_attribute('innerText').replace('\xa0', '')))

        print('List of 1st metric:', metric1_nums)

        # Get Second Metric
        metric_list = driver.find_elements(By.XPATH, '//td[@propertyname="frequencyWs2"]/div/span')
        metric2_nums = []

        for element in metric_list:
            metric2_nums.append(int(element.get_attribute('innerText').replace('\xa0', '')))

        print('List of 2nd metric:', metric2_nums)

    # Get data from json file
    @classmethod
    def test_2A_Get_Data_JSON(cls):

        global metric1_nums_json, metric2_nums_json

        # Parse JSON to variable
        with open("testfile.json", "r", encoding='utf-8') as my_file:
            file = my_file.read()
            file_json = json.loads(file)

        metric1_nums_json = []
        metric2_nums_json = []

        for item in file_json['data']['items']:
            metric1_nums_json.append(int(item['data1']['data2']))
            metric1_nums_json = [numpy.round(x, 2) for x in metric1_nums_json]

            metric2_nums_json.append(int(item['data3']['data4']))
            metric2_nums_json = [numpy.round(x, 2) for x in metric2_nums_json]

        print("List of 1st metric in JSON:", metric1_nums_json)
        print("List of 2nd metric in JSON:", metric2_nums_json)

    # Get data from API request
    @classmethod
    def test_2B_Get_Data_Request(cls):

        global metric1_json, metric2_json

        # API URL
        url = "https://test.in/api/request/1"

        # Read JSON Data for GET request
        file = open('../data.json', 'r')
        json_input = file.read()
        request_json = json.loads(json_input)

        # Make Request
        response = requests.put(url, request_json)

        # Display Response Content
        print(response.content)

        # Parse Response to JSON-Format
        json_response = json.loads(response.text)
        print(json_response)

        metric1_json = []
        metric2_json = []

        for item in json_response['data']['items']:
            metric1_json.append(int(item['data1']['data2']))
            metric1_json = [numpy.round(x, 2) for x in metric1_json]

            metric2_json.append(int(item['data3']['data4']))
            metric2_json = [numpy.round(x, 2) for x in metric2_json]

        print("List of 1st metric in JSON:", metric1_json)
        print("List of 2nd metric in JSON:", metric2_json)

    @classmethod
    def test_3A_Snapshot_Compare_Metric1(cls):

        try:
            # Metric #1
            if not (list(filter(lambda i: i in metric1_nums_json, metric1_nums))):
                print('Data from metric 1 not comparable!\n')

        except Exception:
            assert False, f"Snapshot metric 1 not comparable!"

    @classmethod
    def test_3B_Snapshot_Compare_Metric2(cls):

        try:
            # Metric #2
            if not (list(filter(lambda i: i in metric2_nums_json, metric2_nums))):
                print('Data from metric 2 not comparable!\n')

        except Exception:
            assert False, f"Snapshot metric 2 not comparable!"

    @classmethod
    def tearDownClass(cls):
        driver.quit()


if __name__ == "__main__":
    unittest.main()
