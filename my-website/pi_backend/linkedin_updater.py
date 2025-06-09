
from dotenv import load_dotenv
load_dotenv()

import os
from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/chrisapton/", scrape=True, close_on_complete=True, driver=driver)


# Access top-level info
print("Name:", person.name)
print("Location:", getattr(person, 'location', None))
print("About:", person.about)
print("Open to work:", getattr(person, 'open_to_work', None))
print("Company:", person.company)
print("Job Title:", person.job_title)

print("Experience:")
for exp in person.experiences:
    print(exp)

# add company logo
print("\nEducation:")
for edu in person.educations:
    print(vars(edu))

print("\nCertifications:")
for acc in person.accomplishments:
    print(acc)

# Download resume

# save all the data