import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from .objects import Experience, Education, Scraper, Interest, Accomplishment, Contact

import os
from linkedin_scraper import selectors


class Person(Scraper):

    __TOP_CARD = "main"
    __WAIT_FOR_ELEMENT_TIMEOUT = 10

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        interests=None,
        accomplishments=None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self.also_viewed_urls = []
        self.contacts = contacts or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
        except:
            return False
        
    def focus(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            # No alert to accept, just continue
            pass

    def get_experiences(self):
        url = os.path.join(self.linkedin_url, "details/experience")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)

        with open("linkedin_experience.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
            position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
            elements = position.find_elements(By.XPATH, "*")
            # Not enough data
            if len(elements) < 2:
                continue
                
            company_logo_elem = elements[0]
            position_details = elements[1]

            # company elem
            try:
                company_linkedin_url = company_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
                if not company_linkedin_url:
                    continue
            except NoSuchElementException:
                continue

            # position details
            position_details_list = position_details.find_elements(By.XPATH,"*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            
            if not position_summary_details:
                continue
                
            outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

            if len(outer_positions) == 4:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                location = outer_positions[3].find_element(By.TAG_NAME,"span").text

            # case where it doesn't work with multiple positions in the same compoany
            # potential fix to separate jobs into separate instances
            elif len(outer_positions) == 3:
                if "·" in outer_positions[2].text:
                    position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                    location = ""
                else:
                    # occurs here, the times aren't the correct format, needs cleaning
                    position_title = ""
                    company = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    location = outer_positions[2].find_element(By.TAG_NAME,"span").text

                    print(company)
                    print(work_times)
                    print(location)
            else:
                position_title = ""
                company = outer_positions[0].find_element(By.TAG_NAME,"span").text if outer_positions else ""
                work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text if len(outer_positions) > 1 else ""
                location = ""

            # Safely extract times and duration
            if work_times:
                parts = work_times.split("·")
                times = parts[0].strip() if parts else ""
                duration = parts[1].strip() if len(parts) > 1 else None
            else:
                times = ""
                duration = None

            from_date = " ".join(times.split(" ")[:2]) if times else ""
            to_date = " ".join(times.split(" ")[3:]) if times and len(times.split(" ")) > 3 else ""
            
            if position_summary_text and any(element.get_attribute("class") == "pvs-list__container" for element in position_summary_text.find_elements(By.XPATH, "*")):
                try:
                    inner_positions = (position_summary_text.find_element(By.CLASS_NAME,"pvs-list__container")
                                    .find_element(By.XPATH,"*").find_element(By.XPATH,"*").find_element(By.XPATH,"*")
                                    .find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"))
                except NoSuchElementException:
                    inner_positions = []
            else:
                inner_positions = []

            for pos in inner_positions:
                print(pos)
                print(pos.text)
            
            if len(inner_positions) > 1:
                descriptions = inner_positions
                for description in descriptions:
                    try:
                        res = description.find_element(By.TAG_NAME,"a").find_elements(By.XPATH,"*")
                        position_title_elem = res[0] if len(res) > 0 else None
                        work_times_elem = res[1] if len(res) > 1 else None
                        location_elem = res[2] if len(res) > 2 else None

                        location = location_elem.find_element(By.XPATH,"*").text if location_elem else None
                        position_title = position_title_elem.find_element(By.XPATH,"*").find_element(By.TAG_NAME,"*").text if position_title_elem else ""
                        work_times = work_times_elem.find_element(By.XPATH,"*").text if work_times_elem else ""
                        
                        # Safely extract times and duration
                        if work_times:
                            parts = work_times.split("·")
                            times = parts[0].strip() if parts else ""
                            duration = parts[1].strip() if len(parts) > 1 else None
                        else:
                            times = ""
                            duration = None
                            
                        from_date = " ".join(times.split(" ")[:2]) if times else ""
                        to_date = " ".join(times.split(" ")[3:]) if times and len(times.split(" ")) > 3 else ""

                        experience = Experience(
                            position_title=position_title,
                            from_date=from_date,
                            to_date=to_date,
                            duration=duration,
                            location=location,
                            description=description,
                            institution_name=company,
                            linkedin_url=company_linkedin_url
                        )
                        self.add_experience(experience)
                    except (NoSuchElementException, IndexError) as e:
                        # Skip this description if elements are missing
                        continue
            else:
                description = position_summary_text.text if position_summary_text else ""

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                    description=description,
                    institution_name=company,
                    linkedin_url=company_linkedin_url
                )
                self.add_experience(experience)

    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"):
            try:
                position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
                
                # Fix: Handle case where more than 2 elements are returned
                elements = position.find_elements(By.XPATH,"*")
                if len(elements) < 2:
                    continue  # Skip if we don't have enough elements
                    
                institution_logo_elem = elements[0]
                position_details = elements[1]

                # institution elem
                try:
                    institution_linkedin_url = institution_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
                except NoSuchElementException:
                    institution_linkedin_url = None

                # position details
                position_details_list = position_details.find_elements(By.XPATH,"*")
                position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
                position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
                
                if not position_summary_details:
                    continue
                    
                outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

                institution_name = outer_positions[0].find_element(By.TAG_NAME,"span").text if outer_positions else ""
                degree = outer_positions[1].find_element(By.TAG_NAME,"span").text if len(outer_positions) > 1 else None

                from_date = None
                to_date = None
                
                if len(outer_positions) > 2:
                    try:
                        times = outer_positions[2].find_element(By.TAG_NAME,"span").text

                        if times and "-" in times:
                            split_times = times.split(" ")
                            dash_index = split_times.index("-") if "-" in split_times else -1
                            
                            if dash_index > 0:
                                from_date = split_times[dash_index-1]
                            if dash_index < len(split_times) - 1:
                                to_date = split_times[-1]
                    except (NoSuchElementException, ValueError):
                        from_date = None
                        to_date = None

                description = position_summary_text.text if position_summary_text else ""

                education = Education(
                    from_date=from_date,
                    to_date=to_date,
                    description=description,
                    degree=degree,
                    institution_name=institution_name,
                    linkedin_url=institution_linkedin_url
                )
                self.add_education(education)
            except (NoSuchElementException, IndexError) as e:
                # Skip this education entry if elements are missing
                continue

    def get_name_and_location(self):
        top_panel = self.driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
        self.name = top_panel.find_element(By.TAG_NAME, "h1").text
        self.location = top_panel.find_element(By.XPATH, "//*[@class='text-body-small inline t-black--light break-words']").text

    def get_about(self):
        try:
            about = self.driver.find_element(By.ID,"about").find_element(By.XPATH,"..").find_element(By.CLASS_NAME,"display-flex").text
        except NoSuchElementException :
            about=None
        self.about = about

    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.TAG_NAME,
                    self.__TOP_CARD,
                )
            )
        )
        self.focus()
        self.wait(5)

        # get name and location
        self.get_name_and_location()

        self.open_to_work = self.is_open_to_work()

        # get about
        self.get_about()
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get experience
        self.get_experiences()

        # get education
        self.get_educations()

        driver.get(self.linkedin_url)

        # get interest
        try:

            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            interestContainer = driver.find_element(By.XPATH,
                "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']"
            )
            for interestElement in interestContainer.find_elements(By.XPATH,
                "//*[@class='pv-interest-entity pv-profile-section__card-item ember-view']"
            ):
                interest = Interest(
                    interestElement.find_element(By.TAG_NAME, "h3").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get accomplishments/certifications
        try:
            show_all_spans = driver.find_elements(
                By.XPATH,
                "//span[contains(@class, 'pvs-navigation__text')]"
            )

            target_link = None
            for span in show_all_spans:
                text = span.text.strip()
                if "Show all" in text and "licenses & certifications" in text:
                    # Found it! Go up to the <a>
                    target_link = span.find_element(By.XPATH, "./ancestor::a[1]")
                    break

            if target_link:
                show_all_url = target_link.get_attribute("href")
                print("Navigating to:", show_all_url)
                driver.get(show_all_url)
                print("Found")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-list__item"))
                )

                cert_items = driver.find_elements(By.CLASS_NAME, "artdeco-list__item")
                print(f"Found {len(cert_items)} certifications.")

                for cert in cert_items:
                    cert_dict = {
                        "name": "",
                        "company": "",
                        "date_issued": "",
                        "credential_id": "",
                        "credential_url": "",
                        "company_image_url": "",
                        "skills": []
                    }

                    # Get all unique, stripped lines
                    lines = [line.strip() for line in cert.text.split('\n') if line.strip()]
                    deduped = []
                    for line in lines:
                        if not deduped or deduped[-1] != line:
                            deduped.append(line)

                    # Cert Name (assume first line)
                    cert_dict["name"] = deduped[0] if len(deduped) > 0 else ""

                    # Company Name (second line)
                    cert_dict["company"] = deduped[1] if len(deduped) > 1 else ""

                    # Date Issued
                    for l in deduped:
                        if l.startswith("Issued"):
                            cert_dict["date_issued"] = l.replace("Issued", "").strip()
                            break

                    # Credential ID
                    for l in deduped:
                        if l.startswith("Credential ID"):
                            cert_dict["credential_id"] = l.replace("Credential ID", "").strip()
                            break

                    # Credential URL
                    try:
                        cred_url_elem = cert.find_element(
                            By.XPATH,
                            ".//a[contains(@class, 'optional-action-target-wrapper') and contains(@aria-label, 'Show credential')]"
                        )
                        cert_dict["credential_url"] = cred_url_elem.get_attribute("href")
                    except:
                        cert_dict["credential_url"] = ""


                    # Company image URL
                    try:
                        img_elem = cert.find_element(By.XPATH, ".//img[contains(@class, 'ivm-view-attr__img--centered')]")
                        cert_dict["company_image_url"] = img_elem.get_attribute("src")
                    except:
                        cert_dict["company_image_url"] = ""


                    # Skills: anything after "Skills:" or skill words in lines
                    skill_start = None
                    for i, l in enumerate(deduped):
                        if l.startswith("Skills:"):
                            skill_start = i
                            break
                    if skill_start is not None:
                        cert_dict["skills"] = [s.strip() for s in deduped[skill_start+1:] if s.strip()]
                    else:
                        cert_dict["skills"] = []

                    if (cert_dict["company"] and not cert_dict["company"].startswith("·") and
                            cert_dict["name"] and (cert_dict["date_issued"] or cert_dict["credential_id"])):
                        # prevents it from scraping connections as well
                        self.add_accomplishment(cert_dict)
            else:
                print("Error finding target link")
        

        except:
            print("Error finding accomplishments")
            pass

        # get connections
        # try:
        #     driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        #     _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
        #     )
        #     connections = driver.find_element(By.CLASS_NAME, "mn-connections")
        #     if connections is not None:
        #         for conn in connections.find_elements(By.CLASS_NAME, "mn-connection-card"):
        #             anchor = conn.find_element(By.CLASS_NAME, "mn-connection-card__link")
        #             url = anchor.get_attribute("href")
        #             name = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__name").text.strip()
        #             occupation = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__occupation").text.strip()

        #             contact = Contact(name=name, occupation=occupation, url=url)
        #             self.add_contact(contact)
        # except:
        #     connections = None

        if close_on_complete:
            driver.quit()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return "<Person {name}\n\nAbout\n{about}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nInterest\n{int}\n\nAccomplishments\n{acc}\n\nContacts\n{conn}>".format(
            name=self.name,
            about=self.about,
            exp=self.experiences,
            edu=self.educations,
            int=self.interests,
            acc=self.accomplishments,
            conn=self.contacts,
        )
