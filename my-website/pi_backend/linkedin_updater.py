
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
    # The headless argument is the main one you need for server use
    # options.add_argument("-headless")

    # --- 2. Let Selenium find the geckodriver you installed ---
    # No need for the custom get_chrome_service() function anymore.
    # This will automatically find the geckodriver in /usr/local/bin.
    service = FirefoxService()

    # --- 3. Instantiate the Firefox driver ---
    driver = Firefox(service=service, options=options)

    # --- THIS PART OF YOUR CODE REMAINS EXACTLY THE SAME ---
    # The scraper library interacts with the standard 'driver' object,
    # so it doesn't matter which browser is underneath.

    actions.login(driver, email, password)
    person = Person("https://www.linkedin.com/in/chrisapton/", scrape=True, close_on_complete=False, driver=driver)


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
    