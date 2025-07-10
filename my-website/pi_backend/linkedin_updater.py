
# from dotenv import load_dotenv
# load_dotenv()

import json
import os
# Import the TimeoutException to catch it specifically
from selenium.common.exceptions import TimeoutException

# ---- CHANGE THE IMPORTS ----
# Use classes for Firefox instead of Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

# Your other imports remain the same
from linkedin_scraper import Person, actions


email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

#TODO: 
# Fix education duplication issue

# updates the driver
def update_linkedin():

    options = FirefoxOptions()

    # We MUST run in headless mode for an SSH-only environment
    # options.add_argument("-headless")

    # Explicitly tell Selenium where the Firefox Browser is
    options.binary_location = "/usr/bin/firefox-esr"
    
    driver = None
    try:
        print("Initializing Firefox WebDriver in HEADLESS mode...")
        service = FirefoxService(executable_path="/usr/local/bin/geckodriver")
        driver = Firefox(service=service, options=options)
        
        print("WebDriver initialized successfully!")

        # ... your login and scraping logic goes here ...
        # The error will happen somewhere in this part of the code.


        actions.login(driver, email, password)
        person = Person("https://www.linkedin.com/in/chrisapton/", scrape=True, close_on_complete=False, driver=driver)

    except Exception as e:
        print(f"\n--- An error occurred ---")
        print(f"Error Details: {e}")
        
        if driver:
            # --- THE DEBUGGING STEP FOR SSH ---
            # Save a screenshot of the page where the error happened.
            screenshot_file = "error_screenshot.png"
            driver.save_screenshot(screenshot_file)
            print(f"A screenshot has been saved to your project directory: '{screenshot_file}'")


    # save all the data
    data = {
        "name": person.name,
        "location": getattr(person, 'location', None),
        "about": person.about,
        "company": person.company,
        "jobTitle": person.job_title,
        "resume": person.resume_url
    }

    educations_list = [vars(edu) for edu in person.educations]

    with open('data/about.json', 'w') as f:
        if len(data) != 0:
            json.dump(data, f, indent=4)

    with open("data/experience.json", "w") as f:
        if len(person.experiences) != 0:
            json.dump(person.experiences, f, indent=4)

    with open('data/education.json', 'w') as f:
        if len(educations_list) != 0:
            json.dump(educations_list, f, indent=4)

    with open("data/certifications.json", "w") as f:
        if len(person.accomplishments) != 0:
            json.dump(person.accomplishments, f, indent=4)

def load_linkedin_cache(location):
    file_name = "data/" + location + ".json"
    with open(file_name, "r") as f:
        data = json.load(f)
        return data
    