from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def login(username, password):
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--enable-precise-memory-info')
    # options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    # Navigate to the login page
    driver.get("https://124.123.26.241:1664/merck/login")

    # Find the Username input element and enter your email
    email_input = driver.find_element("css selector", "input[type='text']")
    email_input.send_keys(username)

    # Find the password input element and enter your password
    password_input = driver.find_element("css selector", "input[type='password']")
    password_input.send_keys(password)

    # Submit the form by pressing the Enter key
    password_input.send_keys(Keys.RETURN)

    # Wait for the page to load after submitting the form
    driver.implicitly_wait(10)

    # Verify that the login was successful by checking the URL or page title
    if "Dashboard" in driver.current_url:
        print("Login successful!")
    else:
        print("Login failed.")

    # Close the webdriver
    driver.quit()


login("chaitanya-admin ", "Cohesion_123!")
