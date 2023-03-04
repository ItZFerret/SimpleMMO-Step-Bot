import time
import sys
import os
import winsound
import win10toast
import win11toast
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from win11toast import toast

# Get the PID of the current Python process
pid = os.getpid()

# Write the PID to a text file
with open("pid.txt", "w") as f:
    f.write(str(pid))

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
            print(f"That's {item_count} items found this session! Don't forget to check your inventory.")
    except:
        pass
    with open("ItemsFound.txt", "w") as f:
        f.write(f"{item_store} items found in this session!")

    # Print "looping..." and wait for 3 seconds before restarting the loop
    loop_count += 1
    step_store += 1
    with open("steps.txt", "w") as f:
        f.write(f"{step_store} steps taken this session!")
    print("stepping...")
    time.sleep(3)
    print(f"{loop_count} steps taken in current session!")


# Close the driver when the loop is finished
driver.quit()
