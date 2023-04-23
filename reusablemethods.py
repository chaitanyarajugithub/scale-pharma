import time
import psutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import datetime
import os

# Set the timeout and interval variables
timeout = 30
interval = 1

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


def selectdevicetype(devicetype, driver):
    if 'cond' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:nth-child(3) [type="button"]').click()
    elif 'ph' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:last-child [type="button"]').click()
    elif 'balance' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:nth-child(2) [type="button"]').click()
    elif 'apc' in devicetype.lower():
        driver.find_element('css selector', 'div.col-lg-3:nth-child(1) [type="button"]').click()


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


def servermemory():
    # Getting % usage of virtual_memory ( 3rd field)
    print('RAM memory % used:', psutil.virtual_memory()[2])
    return psutil.virtual_memory()[2]


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


def getcurrent_time():
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime


def searchresultsapc(text, driver):
    search_box = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'table tr:nth-child(1) th:nth-child(7) input')))
    search_box.clear()
    search_box.send_keys(text)
    element = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//table//tr[1]//th[7]//*[contains(@class, 'material-icons') and contains(@class, 'q-icon') and contains(text(), 'search')]")))
    # Click on the element
    element.click()
    time.sleep(3)

def clickonstart(driver):
    startbutton = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "// *[contains(text(), 'START')]")))
    # Click on the element
    startbutton.click()

def chooseequipment(driver, serielnumber):
    # Wait for the element with class 'tab-btn-dis' to disappear
    WebDriverWait(driver, timeout, interval).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'tab-btn-dis')))

    # Check if the text 'CHOOSE EQUIPMENT' is visible
    WebDriverWait(driver, timeout, interval).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'CHOOSE EQUIPMENT'))
    time.sleep(5)
    # Check if the element with selector 'adhocele.choosequipment.choosequipment' exists and click on it if it does, otherwise click on '.continuous-run .tab-btn'
    try:
        driver.find_element(By.CSS_SELECTOR, '.tab-default').click()
    except:
        WebDriverWait(driver, timeout, interval).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.continuous-run .tab-btn')))
        driver.find_element(By.CSS_SELECTOR, '.continuous-run .tab-btn').click()

    # Wait for the button in the step container to be disabled, check the checkbox, wait for the button to be enabled, and click on it
    WebDriverWait(driver, timeout, interval).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.stepContainer button')))
    WebDriverWait(driver, timeout, interval).until_not(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.stepContainer button')))
    time.sleep(4)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, '.q-checkbox__bg')
    for checkbox in checkboxes:
        time.sleep(1)
        checkbox.click()
    time.sleep(5)
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.stepContainer button')))
    driver.find_element(By.CSS_SELECTOR, '.stepContainer button').click()

    # Enter the serial number and search, wait for the table to load, and click on the checkbox and button
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Likely Search"]').send_keys(serielnumber)
    driver.find_element(By.CSS_SELECTOR, '[style="cursor: pointer;"]').click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '.q-table tbody tr td .q-checkbox').click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[contains(text(),'NEXT')]").click()
    time.sleep(3)
    # Click on the button
    WebDriverWait(driver, timeout, interval).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'CONFIRM')]")))
    driver.find_element(By.XPATH, "//div[contains(text(),'CONFIRM')]").click()
    time.sleep(3)

def startsceduledsample(driver):
    # Wait for the "START" button to be enabled and click it
    WebDriverWait(driver, timeout, interval).until(EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(), 'START')]")))
    driver.find_element('xpath', "//button[@type='button']").click()
    time.sleep(3)
    # Wait for the form to be visible
    form = WebDriverWait(driver, timeout, interval).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form.q-form")))

    # Click on the second q-select element and select "Static"
    select = form.find_elements(By.CSS_SELECTOR, ".q-select")[1]
    select.click()
    static_option = WebDriverWait(driver, timeout, interval).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Static')]")))
    static_option.click()

    # Click on the "Confirm sample" button
    confirm_button = WebDriverWait(driver, timeout, interval).until(EC.element_to_be_clickable((By.XPATH, "//button//div[contains(text(), 'Confirm sample')]")))
    confirm_button.click()
    time.sleep(10)


def confirm_result(driver):
    # Wait for the first '.ignore-single-status.single-status' element containing 'Sampling'
    sampling_element = WebDriverWait(driver, timeout, interval).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".ignore-single-status.single-status"), "Sampling"))
    # Wait for the dialog container to exist
    dialog_container = WebDriverWait(driver, 100, interval).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dialog-container")))
    time.sleep(3)
    # Click the "Confirm Result" button
    confirm_button = WebDriverWait(driver, timeout, interval).until(EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(), 'Confirm Result')]")))
    driver.find_element('xpath', "//button//*[contains(text(), 'Confirm Result')]").click()
    time.sleep(3)


def finishmeasure(driver, operatoruser):
    actions = ActionChains(driver)
    textareaelement = WebDriverWait(driver, timeout, interval).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea")))
    time.sleep(1)
    actions.move_to_element(textareaelement).perform()
    time.sleep(1)
    driver.find_element('css selector', 'textarea').send_keys(
        ' '.join(random.choices(string.ascii_letters + string.digits, k=3)))
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li:nth-child(1) .ignore-sample-setting-select .column"))).click()
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Yes')]"))).click()
    time.sleep(1)
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li:nth-child(2) .ignore-sample-setting-select .column"))).click()
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Yes')]"))).click()
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(), 'Confirm')]")))
    driver.find_element('xpath', "//button//*[contains(text(), 'Confirm')]").click()
    time.sleep(4)
    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.justify-end button')))
    driver.find_element('css selector', '.justify-end button').click()
    time.sleep(3)
    WebDriverWait(driver, timeout, interval).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea")))
    time.sleep(1)
    driver.find_element('css selector', 'textarea').send_keys(
        ' '.join(random.choices(string.ascii_letters + string.digits, k=3)))


    # Type the value of 'user' into the first input element matching '.q-card__section input'
    WebDriverWait(driver, timeout, interval).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".q-card__section input")))[0].send_keys(operatoruser)

    # Type the value 'Cohesion_123!' into the second input element matching '.q-card__section input'
    WebDriverWait(driver, timeout, interval).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".q-card__section input")))[1].send_keys("Cohesion_123!")

    WebDriverWait(driver, timeout, interval).until(
        EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(), 'Submit')]")))
    driver.find_element('xpath', "//button//*[contains(text(), 'Submit')]").click()
    time.sleep(5)