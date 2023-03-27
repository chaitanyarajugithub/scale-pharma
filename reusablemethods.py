import time
import psutil
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

