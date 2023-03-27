from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
import string


def test_operator_login(username, serielnumber):
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    options.add_argument('--no-close')
    driver = webdriver.Chrome(executable_path='/Users/chaitanya/Downloads/Selenium/Installers/Drivers/chromedriver_copy', options=options)
    driver.get("https://124.123.26.241:1665/merck/login")
    driver.maximize_window()
    driver.find_element("css selector", "input[type='text']").click()
    driver.find_element("css selector", "input[type='text']").clear()
    driver.find_element("css selector", "input[type='text']").send_keys(username)
    driver.find_element("css selector", "input[type='password']").clear()
    driver.find_element("css selector", "input[type='password']").send_keys('Cohesion_123!')
    driver.find_element("css selector", ".loginBtn").click()
    time.sleep(10)
    driver.find_element('css selector', 'div.col-lg-3:last-child [type="button"]').click()
    # Wait for element with class 'loadingContent' to exist
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'loadingContent')))
    print("Navigated to Measure")
    # Wait for element with class 'loadingContent' to not exist
    WebDriverWait(driver, 40).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'loadingContent')))
    time.sleep(2)
    print("Search Device and select")
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
    print("Navigates to Step3")
    for i in range(1, 10):
        print("Ph measure iteration Start "+str(i))
        WebDriverWait(driver, 40).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.renderedStatus.statusAlign'), 'Ready'))
        print("Select PhMeasure and start")
        # Find the dropdown element
        dropdown_element = driver.find_element('xpath',
                                               "//div[@id='q-app']/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div/div/div/div/div/div/div/div[2]/div/select")
        # Create a Select object and select an option by its visible text
        select = Select(dropdown_element)
        dropdown_element.click()
        select.select_by_visible_text("pH MEAS")
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
        driver.find_element('xpath', "//*[contains(text(),'Abort')]/ancestor::button").click()
        result_textarea = WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.result-textarea textarea')))
        result_textarea.send_keys(' '.join(random.choices(string.ascii_letters + string.digits, k=3)))
        # Click the primary button
        primary_button = driver.find_element(By.CSS_SELECTOR, 'button.bg-primary.common-btn')
        primary_button.click()
        time.sleep(8)
        print("Navigates to Step 4")
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Confirm')]/ancestor::button")))
        driver.find_element('xpath', "//*[contains(text(),'Confirm')]/ancestor::button").click()
        time.sleep(10)
        print("Ph measure iteration End "+str(i))
    WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Release')]/ancestor::button")))
    driver.find_element('xpath', "//*[contains(text(),'Release')]/ancestor::button").click()
    time.sleep(10)
    print("END")
    driver.quit()


if __name__ == '__main__':
    # create a list of tuples containing the user login credentials
    users = [('Chaitanya-operator', 'SE000054'), ('Akanksha-operator', 'SE000055'),
             ('phz-op701', 'SE000056'), ('phz-op702', 'SE000057'),
             ('phz-op703', 'SE000058'), ('phz-op704', 'SE000059'),
             ('phz-op705', 'SE000060'), ('phz-op706', 'SE000061'),
             ('phz-op707', 'SE000062'), ('phz-op708', 'SE000063')]

    # create a list of processes to run the test with each user login in a separate browser
    processes = []
    for user in users:
        p = Process(target=test_operator_login, args=user)
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()
