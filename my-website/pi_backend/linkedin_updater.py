
# from dotenv import load_dotenv
# load_dotenv()

import os
import json
from linkedin_scraper import Person, actions
from selenium import webdriver

email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

# updates the driver

def update_linkedin():
    driver = webdriver.Chrome()
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
    