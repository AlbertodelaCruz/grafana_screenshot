from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from decouple import config
from slack_sdk import WebClient

GRAFANA_URL = config('GRAFANA_URL')
GRAFANA_USERNAME = config('GRAFANA_USERNAME')
GRAFANA_PASSWORD = config('GRAFANA_PASSWORD')
SLACK_BOT_TOKEN = config('SLACK_BOT_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')
BASE_URL = '/'.join(GRAFANA_URL.split('/')[0:3])

# Webdrive config
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)

# Maximize the browser window
driver.maximize_window()

# Navigate to the login page
login_url = f'{BASE_URL}/login'
driver.get(login_url)

# Wait for the username field to be present on the page
username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'user'))
)

# Locate the username and password fields and submit button
password_field = driver.find_element(By.NAME, 'password')  # replace with the actual name of the password field
submit_button = driver.find_element(By.CLASS_NAME, 'css-1l65ky1-button')  # replace with the actual name of the submit button

# Enter your login credentials
username_field.send_keys(GRAFANA_USERNAME)
password_field.send_keys(GRAFANA_PASSWORD)

# Click the submit button
submit_button.click()


# Wait for the URL to change after login
WebDriverWait(driver, 10).until(
        EC.url_changes(login_url)
)

# Wait for the login to complete (you may need to customize this wait based on your application)
#driver.implicitly_wait(10)

# Navigate to the desired URL
driver.get(GRAFANA_URL)

#wait to load page
time.sleep(5)

# Take a screenshot of the entire page
driver.save_screenshot('screenshot.png')

# Close the browser
driver.quit()


## Post file to slack
client = WebClient(SLACK_BOT_TOKEN)

# Tests to see if the token is valid
auth_test = client.auth_test()
bot_user_id = auth_test["user_id"]
print(f"App's bot user: {bot_user_id}")

upload_text_file = client.files_upload_v2(
        channels=SLACK_CHANNEL,
        title="Screenshot",
        file="./screenshot.png",
        initial_comment="Screenshot!!",
)

