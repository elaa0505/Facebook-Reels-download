from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Author Elango Saminathan
# Mail elaaisolution@gmail.com

import time

# Facebook Login Credentials (Replace with your details)
USERNAME = "fbusername"
PASSWORD = "fbuserpass"

# Path to Chrome WebDriver (Update the path)
CHROME_DRIVER_PATH = "\\chromedriver.exe"

# Facebook Reel URL
REEL_URL = "Reels Page URL"

# Number of reels to scrape
MAX_REELS = 1000

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Open in full screen
options.add_argument("--disable-notifications")  # Disable pop-ups

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Open Facebook Reel
driver.get(REEL_URL)
time.sleep(5)  # Wait for page to load

# Log in to Facebook
email_field = driver.find_element(By.XPATH, "(//*[@name='email'])[2]")
password_field = driver.find_element(By.XPATH, "(//*[@name='pass'])[2]")

email_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)
time.sleep(25)  # Wait for login

# Click Share button
share_button = driver.find_element(By.XPATH, "(//a[@aria-label='Reel tile preview'])[1]")
share_button.click()
time.sleep(3)

# Open file to save reel links
with open("reel_links.txt", "w", encoding="utf-8") as file:
    for i in range(MAX_REELS):
        try:
            
            
            # Click Share button
            share_button = driver.find_element(By.XPATH, "//div[@aria-label='Share']")
            share_button.click()
            time.sleep(3)

            # Click Copy Link
            copy_link_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Copy link')]")
            copy_link_button.click()
            time.sleep(2)
            
             # Click Copy Link
            try:
                copy_link_button = driver.find_element(By.XPATH, "(//span[@dir='auto']/div)[2]")
                if copy_link_button:  # If list is not empty
                    title = copy_link_button.text  # Get first matching element
                    print("✅ Element Found:", copy_link_button.text)
            except:
                title = "NULL"
                print("null")  # Print "null" if element is not found
            
            
            #print(title)
            time.sleep(2)
            
            # Click Copy Link
            #copy_link_button = driver.find_element(By.XPATH, "(//div[@aria-label='Close'])[last()]")
            #copy_link_button.click()
            #time.sleep(2)

            # Get copied link from clipboard (Windows)
            import pyperclip
            reel_link = pyperclip.paste()

            # Save to file
            file.write(f"{reel_link}\t")
            file.write(f"{title}\n")
            print(f"✅ Saved Reel {i+1}: {reel_link} {title}")

            # Click Next Reel Button
            next_reel_button = driver.find_element(By.XPATH, "(//div[@aria-label='Next card'])[last()]")
            next_reel_button.click()
            time.sleep(5)  # Wait for next reel to load

        except Exception as e:
            print(f"❌ Error on Reel {i+1}: {e}")
            break

# Close the browser
driver.quit()
print("✅ Task Completed!")
