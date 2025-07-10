
# from dotenv import load_dotenv
# load_dotenv()

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from linkedin_scraper import Person, actions
import os
import json

email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")



#TODO: 
# Fix education duplication issue

# updates the driver
def update_linkedin():
    # Set up Chrome options
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"  # or "/usr/bin/chromium"
    options.add_argument("--headless")                     # (optional)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up the service
    service = Service("/usr/bin/chromedriver")

    # Create the driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)  # seconds
    actions.login(driver, email, password)
    person = Person("https://www.linkedin.com/in/chrisapton/", scrape=True, close_on_complete=True, driver=driver)

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
    