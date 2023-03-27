# This is a sample Python script.

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time


class OperatorLogin(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []

    def test_operator_login(self):
        options = Options()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-close')  # Prevents the browser from closing
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='/Users/chaitanya/Downloads/Selenium/Installers/Drivers/chromedriver_copy', options=options)
        # driver = webdriver.Chrome("/Users/chaitanya/Downloads/Selenium/Installers/Drivers/chromedriver_copy")
        driver.get("https://124.123.26.241:1665/merck/login")
        driver.maximize_window()
        time.sleep(10)
        driver.find_element("css selector", "input[type='text']").click()
        driver.find_element("css selector", "input[type='text']").clear()
        driver.find_element("css selector", "input[type='text']").send_keys("Chaitanya-operator")
        driver.find_element("css selector", "input[type='password']").clear()
        driver.find_element("css selector", "input[type='password']").send_keys("Cohesion_123!")
        driver.find_element("css selector", ".loginBtn").click()
        time.sleep(10)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
