import time
import psutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import os

def login(username,driver):
    driver.find_element("css selector", "input[type='text']").click()
    driver.find_element("css selector", "input[type='text']").clear()
    driver.find_element("css selector", "input[type='text']").send_keys(username)
    driver.find_element("css selector", "input[type='password']").clear()
    driver.find_element("css selector", "input[type='password']").send_keys('Cohesion_123!')
    driver.find_element("css selector", ".loginBtn").click()
    time.sleep(10)


def logout(driver):
    driver.find_element("css selector", ".logout > .q-tab__content > .tab-item > .ignore-plan-icon").click()
    time.sleep(4)
    driver.find_element("css selector", ".confirmDialog>.justify-center>button:first-of-type").click()
    start_time = time.time()
    while 'merck/login' not in driver.current_url:
        time.sleep(1)
        if time.time() > start_time + 10:
            raise Exception('Timeout: Login page not loaded')
    time.sleep(2)


def selectdevicetype(devicetype,driver):
    if 'cond' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:nth-child(3) [type="button"]').click()
    elif 'ph' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:last-child [type="button"]').click()
    elif 'balance' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:nth-child(2) [type="button"]').click()


def cpuutilization():
    # get CPU utilization as a percentage
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def memoryutilization(driver):
    # execute JavaScript to get the memory usage data
    memory_data = driver.execute_script("return window.performance.memory")
    # extract the value of the 'usedJSHeapSize' property
    used_js_heap_size = memory_data['usedJSHeapSize']
    return used_js_heap_size

def abortmeasure(driver):
    driver.find_element('xpath', "//*[contains(text(),'Abort')]/ancestor::button").click()
    time.sleep(2)
    result_textarea = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.result-textarea textarea')))
    result_textarea.send_keys(' '.join(random.choices(string.ascii_letters + string.digits, k=3)))
    time.sleep(1)
    # Click the primary button
    primary_button = driver.find_element(By.CSS_SELECTOR, 'button.bg-primary.common-btn')
    primary_button.click()


def resetdevice(driver,serielnumber):
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
    WebDriverWait(driver, 40).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.balance-card-header-light-red')))

