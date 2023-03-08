import time
import sys
import os
import winsound
import random
import string
import win10toast
import win11toast
import requests
import json
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from win11toast import toast

with open('webhook.txt', 'r') as f:
    DISCORD_WEBHOOK_URL = f.read().strip()

# Load the user agent from agent.txt
with open("agent.txt") as f:
    user_agent = f.read().strip()

# Load the saved user login from login.txt
if os.path.exists("login.txt"):
    with open("login.txt") as f:
        lines = f.readlines()
        email = lines[0].strip()
        password = lines[1].strip()
        time_limit_hours = int(lines[2].strip()) # Change this line
else:
    # prompt the user to enter their login info
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    time_limit_hours = int(input("Enter the time limit in hours: ")) # Change this line
    # save the users input to login.txt for next launch
    with open("login.txt", "w") as f:
        f.write(f"{email}\n{password}\n{time_limit_hours}")

# Set up the Chrome driver with the undetected chrome module
options = ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
driver = Chrome(options=options)

# Navigate to the login page
driver.get("https://web.simple-mmo.com/login")

# Wait for the email field to be visible
email_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "email"))
)

# Enter the user's email from file or user input
email_field.send_keys(email)

# Wait for the password field to be visible
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "password"))
)

# Enter the user's password from file or user input
password_field.send_keys(password)


# Wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)

# Click the login button
login_button.click()

# Wait for the page to load
time.sleep(3)

# Navigate to the travel page
driver.get("https://web.simple-mmo.com/travel")

print("Welcome to SimpleMMO Stepper!")
toast('Welcome to SimpleMMO Stepper!')
message = {
    'content': f'SimpleStepper has started. You will receive a ping if verification is detected.'
}
# Send the message to Discord
response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(message),
                         headers={'Content-Type': 'application/json'})
print(f"Discord notification sent with status code {response.status_code}")

# Wait for the page to load
time.sleep(3)

# Wait for the step button to be clickable
step_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "step_button"))
)


loop_count = 0 # tracking the number of steps taken with the bot
item_count = 0 # tracking the number of items found with the bot
item_store = 0 # storing amount of items found with the bot in one session
step_store = 0 # storing amount of steps in one session

rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
toaster = ToastNotifier()

# Calculate the time at which the loop should stop
stop_time = time.time() + time_limit_hours * 3600

while time.time() < stop_time:
    try:
        if step_button.is_enabled():
            step_button.click()
            time.sleep(3)
    except:
        pass

    # Wait for 5 seconds before checking for the perform verification button
    print("checking for verification...")
    time.sleep(5)
    print("small delays help to avoid detection, please be patient...")

    try:
       captcha_link = driver.find_element(By.XPATH, "//*[text()='Perform Verification']")
       if captcha_link.is_displayed():
            print("Solve the captcha to continue, if you are done solving, type C to continue the loop.")
            alert_sound()
            toast("Verification Detected", "Solve the captcha to continue stepping")
            message = {
                'content': f'Verification Detected! Solve the captcha to continue stepping'
            }
            # Send the message to Discord
            response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(message),
                                     headers={'Content-Type': 'application/json'})
            print(f"Discord notification sent with status code {response.status_code}")
            while True:
                if input().lower() == "c":
                    break
    except:
        pass

    # Check for the "You have found an item!" text and print "you found an item!" to the console if it is present
    try:
        found_item = driver.find_element(By.XPATH, "//*[text()='You have found an item!']")
        if found_item.text == "You have found an item!":
            print("You found an item!")
            item_count += 1
            item_store += 1
            message = {
                'content': f'You have found an item! Thats {item_store} this session!'
            }
            # Send the message to Discord
            response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(message),
                                     headers={'Content-Type': 'application/json'})
            print(f"Discord notification sent with status code {response.status_code}")
            file_name = (f'item_{rand_str}.png')
            print(f"That's {item_count} items found this session! Don't forget to check your inventory. Screenshot saved.")
            folder_path = os.path.join(os.getcwd(), 'pages/items')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, file_name)
            driver.save_screenshot(file_path)
    except:
        pass
    with open("ItemsFound.txt", "w") as f:
        f.write(f"{item_store} items found in this session!")


    # Print "stepping..." and wait for 3 seconds before restarting the loop
    loop_count += 1
    step_store += 1
    with open("steps.txt", "w") as f:
        f.write(f"{step_store} steps taken this session!")
    print("stepping...")
    time.sleep(3)
    print(f"{loop_count} steps taken in current session!")


    with open("status.txt", "r") as f:
        status = f.readline().strip()

    if status == "pause":
        print("Script is paused")
        while True:
            time.sleep(1)
            with open("status.txt", "r") as f:
                status = f.readline().strip()
            if status == "resume":
                print("Script is resumed")
                break
    elif status == "resume":
        # Put your script code here
        time.sleep(1)
    else:
        print("Invalid status in status.txt")
        break


# Close the driver when the loop is finished
driver.quit()
