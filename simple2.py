import time
import sys
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Load the user agent from agent.txt
with open("agent.txt") as f:
    user_agent = f.read().strip()

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

# Prompt the user to enter their login information
email = input("Enter your email: ")
password = input("Enter your password: ")

# Enter the user's email
email_field.send_keys(email)

# Wait for the password field to be visible
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "password"))
)

# Enter the user's password
password_field.send_keys(password)

# Save the user's login information to login.txt
with open("login.txt", "w") as f:
    f.write(f"{email}\n{password}")

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

# Wait for the page to load
time.sleep(3)

# Wait for the step button to be clickable
step_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "step_button"))
)

while True:
    try:
        if step_button.is_enabled():
            step_button.click()
            time.sleep(3)
    except:
        pass

    # Wait for 5 seconds before checking for the perform verification button
    print("checking for verification...")
    print("small delays help to avoid detection, please be patient...")
    time.sleep(5)

    try:
       captcha_link = driver.find_element(By.XPATH, "//*[text()='Perform Verification']")
       if captcha_link.is_displayed():
            print("Solve the captcha to continue, if you are done solving, type C to continue the loop.")
            while True:
                if input().lower() == "c":
                    break
    except:
        pass

    # Check for the "You have found an item!" text and print "you found an item!" to the console if it is present
    try:
        travel_heading = driver.find_element(By.XPATH, "//*[text()='You have found an item!']")
        if travel_heading.text == "You have found an item!":
            print("You found an item!")
    except:
        pass

    # Print "looping..." and wait for 3 seconds before restarting the loop
    print("looping...")
    time.sleep(3)

# Close the driver when the loop is finished
driver.quit()
