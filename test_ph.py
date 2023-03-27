from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, \
    ElementNotVisibleException
import time
import random
import string
import csv
import psutil
from db import query_database
from reusablemethods import *
import colorama
from colorama import Fore

users = []
devicetype = 'Conductivity'
testtype = 'Complete'


def test_operator_login(adminuser, operatoruser, serielnumber):
    try:
        # Call the query_database method from file1.py
        results = query_database(serielnumber)
        action_status = results[0][0]
        print(operatoruser, '-->', serielnumber, '-->', results[0][0])
        options = Options()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument('--enable-precise-memory-info')
        # options.add_argument('--no-close')
        # options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        driver.get("https://124.123.26.241:1665/merck/login")
        driver.maximize_window()
        if "out" in action_status:
            print(adminuser, '-->', serielnumber, '-->', "Reset Device")
            login(adminuser, driver)
            selectdevicetype(devicetype, driver)
            time.sleep(10)
            print(adminuser, '-->', serielnumber, '-->', "Search Device and select")
            # Locate the search box and clear its contents before typing in the text
            search_box = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Likely Search"]')))
            search_box.clear()
            search_box.send_keys(serielnumber)
            # Click on the search button
            search_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.q-field__append > :nth-child(2)')))
            search_button.click()
            time.sleep(10)
            reset_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Reset"]')))
            reset_button.click()
            time.sleep(3)
            result_textarea = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.run-commnet textarea')))
            result_textarea.send_keys(' '.join(random.choices(string.ascii_letters + string.digits, k=3)))
            time.sleep(3)
            reset_button = driver.find_element("css selector", '.col-6:nth-child(2) .balance-primary-button')
            actions = ActionChains(driver)
            # move to the element
            actions.move_to_element(reset_button).perform()
            reset_button.click()
            time.sleep(3)
            print(adminuser, '-->', serielnumber, '-->', "Reset Done")
            WebDriverWait(driver, 40).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.balance-card-header-light-red')))
            logout(driver)
        else:
            print(serielnumber, '-->', "Device checked-in --> Proceed with tests")
        login(operatoruser, driver)
        time.sleep(10)
        print(operatoruser, '-->', serielnumber, '-->', 'Operator Login Successful')
        selectdevicetype(devicetype, driver)
        # Wait for element with class 'loadingContent' to exist
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'loadingContent')))
        print(operatoruser, '-->', serielnumber, '-->', "Navigated to Measure")
        # Wait for element with class 'loadingContent' to not exist
        WebDriverWait(driver, 40).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'loadingContent')))
        time.sleep(2)
        print(operatoruser, '-->', serielnumber, '-->', "Search Device and select for check-out")
        # Locate the search box and clear its contents before typing in the text
        search_box = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Search"]')))
        search_box.clear()
        search_box.send_keys(serielnumber)
        # Click on the search button
        search_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.q-field__append > :nth-child(2)')))
        search_button.click()
        time.sleep(5)
        table_element = driver.find_element("css selector", '.q-table')
        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'td:nth-child(3) div[style=""] span')))
        table_element.find_element('xpath', f"//td[contains(.,'{serielnumber}')]/preceding-sibling::td[1]").click()
        WebDriverWait(driver, 40).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.balance-primary-button'), 'Next'))
        driver.find_element('css selector', '.balance-primary-button').click()
        WebDriverWait(driver, 40).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.balance-primary-button'), 'Confirm'))
        driver.find_element('css selector', '.balance-primary-button').click()
        print(operatoruser, '-->', serielnumber, '-->', "Navigates to Step3")
        for i in range(1, 200):
            print(Fore.WHITE + operatoruser, '-->', serielnumber, '-->', "Ph measure iteration Start " + str(i))
            WebDriverWait(driver, 40).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.renderedStatus.statusAlign'), 'Ready'))
            print(operatoruser, '-->', serielnumber, '-->', "Select PhMeasure and start")
            # Find the dropdown element
            dropdown_element = driver.find_element('xpath',
                                                   "//div[@id='q-app']/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div/div/div/div/div/div/div/div[2]/div/select")
            # Create a Select object and select an option by its visible text
            select = Select(dropdown_element)
            dropdown_element.click()
            if 'ph' in devicetype.lower():
                select.select_by_visible_text("pH MEAS")
            elif 'cond' in devicetype.lower():
                select.select_by_visible_text("Cond Meas")
            # Generate a random string of length 8
            time.sleep(2)
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            driver.find_element('xpath', "//input[@type='text']").send_keys(random_string)
            time.sleep(2)
            WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Start')]/ancestor::button")))
            driver.find_element('xpath', "//*[contains(text(),'Start')]/ancestor::button").click()
            time.sleep(4)
            WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'protocolsTableHeaders')))
            WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Abort')]/ancestor::button")))
            time.sleep(2)
            driver.find_element('xpath', "//*[contains(text(),'Abort')]/ancestor::button").click()
            time.sleep(2)
            result_textarea = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.result-textarea textarea')))
            result_textarea.send_keys(' '.join(random.choices(string.ascii_letters + string.digits, k=3)))
            time.sleep(1)
            # Click the primary button
            primary_button = driver.find_element(By.CSS_SELECTOR, 'button.bg-primary.common-btn')
            primary_button.click()
            time.sleep(15)
            print(operatoruser, '-->', serielnumber, '-->', "Navigates to Step 4")
            WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Confirm')]/ancestor::button")))
            time.sleep(5)
            driver.find_element('xpath', "//*[contains(text(),'Confirm')]/ancestor::button").click()
            time.sleep(20)
            print(operatoruser, '-->', serielnumber, '-->', "Ph measure iteration End " + str(i))
            # CPU and Memory Utilization
            cpu_percent = cpuutilization()
            used_js_heap_size = memoryutilization(driver)
            # print the results
            print(operatoruser, '-->', serielnumber, '-->', "Total CPU utilization: {}%".format(cpu_percent))
            print(operatoruser, ' After ', i, 'Measures-->',
                  "Used JS Heap Size: {} MB".format(used_js_heap_size / (1024 * 1024)))
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Release')]/ancestor::button")))
        driver.find_element('xpath', "//*[contains(text(),'Release')]/ancestor::button").click()
        time.sleep(10)
        print(operatoruser, '-->', serielnumber, '-->', "END")
        # driver.quit()
    except (Exception, ElementClickInterceptedException, NoSuchElementException, TimeoutException,
            ElementNotVisibleException) as e:
        # Handle the exception
        print(Fore.RED + "Got an Error", e)
    finally:
        # Close the browser
        # driver.quit()
        pass


if __name__ == '__main__':
    # open the CSV file and read the data
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        for row in reader:
            # append a tuple of operatoruser and password to the users list
            users.append((row[0], row[1], row[2]))

    # create a list of processes to run the test with each user login in a separate browser
    processes = []
    for user in users:
        p = Process(target=test_operator_login, args=user)
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()
