from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reusablemethods import *
from soapconnector import *
import csv
from multiprocessing import Process
import colorama
from colorama import Fore

users = []
devicetype = "APC"

def sceduledsample(operatoruser, serielnumber):
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--auto-open-devtools-for-tabs")
    # options.add_argument('--headless')
    options.add_argument('--enable-precise-memory-info')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    # Navigate to the login page
    driver.get("https://124.123.26.241:1664/merck/login")
    driver.maximize_window()
    time.sleep(5)
    print(operatoruser, '--> Test Execution Start -->', getcurrent_time())
    # Login
    login(operatoruser, driver)
    time.sleep(5)
    print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Operator Login Successful')
    # Select device type
    selectdevicetype('apc', driver)
    print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Particle Counter Selected')
    time.sleep(5)
    # Add Scheduled Sample
    filedata = createdata(operatoruser)
    print(filedata['SampleNumber'])
    addsceduledsample('http://172.168.9.147', filedata)
    print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Scheduled sample added')
    for i in range(1, 200):
        print(Fore.WHITE + getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', devicetype,
              " measure iteration Start " + str(i))
        # Navigates to Equipment Page
        driver.find_element('css selector', '[href="/merck/particle_counter/auditing"]').click()
        print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Navigated to Auditing Page')
        time.sleep(5)
        driver.find_element('css selector', '[placeholder="Likely Search"]').click()
        driver.find_element('css selector', '[placeholder="Likely Search"]').clear()
        driver.find_element('css selector', '[placeholder="Likely Search"]').send_keys(serielnumber)
        time.sleep(1)
        for c in range(1, 500):
            time.sleep(2)
            driver.find_element('xpath', "//i[contains(text(),'search')]").click()
            cpu_percent = cpuutilization()
            used_js_heap_size = memoryutilization(driver)
            # print the results
            print(operatoruser, '-->', serielnumber, '-->', "Total CPU utilization: {}%".format(cpu_percent))
            print(operatoruser, ' After ', c, 'Search Clicks-->',
                  "Used JS Heap Size: {} MB".format(used_js_heap_size / (1024 * 1024)))
        time.sleep(3)
        occupiedele = driver.find_elements('css selector', 'tr .usingProp')
        if len(occupiedele) > 0:
            print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Device Locked/ Occupied')
            driver.find_element('css selector', '[href="/merck/particle_counter/measure"]').click()
            time.sleep(3)
        else:
            print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Device not Occupied Proceed with test ', i)
            # Navigates to Measure Page
            driver.find_element('css selector', '[href="/merck/particle_counter/measure"]').click()
            time.sleep(3)
            # Navigates to Scheduled sample
            searchresultsapc(filedata['SampleNumber'], driver)
            time.sleep(5)
            # Start Scheduled Sample
            clickonstart(driver)
            # Choose Equipment
            chooseequipment(driver, serielnumber)
            # # Start Measure
            # startsceduledsample(driver)
            # print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', 'Scheduled sample Started')
            # # Complete measure
            # confirm_result(driver)
            # # Finish Measure
            # finishmeasure(driver, operatoruser)
            print(getcurrent_time(), '-->', operatoruser, '-->', serielnumber, '-->', devicetype,
                  " measure iteration End " + str(i))
            # CPU and Memory Utilization
            cpu_percent = cpuutilization()
            used_js_heap_size = memoryutilization(driver)
            # print the results
            print(operatoruser, '-->', serielnumber, '-->', "Total CPU utilization: {}%".format(cpu_percent))
            print(operatoruser, ' After ', i, 'Measures-->',
                  "Used JS Heap Size: {} MB".format(used_js_heap_size / (1024 * 1024)))
    print(operatoruser, '--> Test Execution End -->', getcurrent_time())
    # Close the webdriver
    driver.quit()


if __name__ == '__main__':
    # open the CSV file and read the data
    with open('users_apc.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header row
        for row in reader:
            # append a tuple of operatoruser and password to the users list
            users.append((row[0], row[1]))

    # create a list of processes to run the test with each user login in a separate browser
    processes = []
    for user in users:
        p = Process(target=sceduledsample, args=user)
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()
