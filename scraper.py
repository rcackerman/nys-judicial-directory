import time
import string
import re
import csv
import json
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_alphabet_list(driver, letter):
    """Use the letter given to determine what directory page to go to,
    then scrape and return a list of each judge on the page
    """
    browser.find_element_by_link_text(letter).click()

    # Each alphabetized page has links to the judges, which we will record
    _ = browser.find_elements_by_xpath("//a[contains(@href, 'JUDGE_ID')]")
    return [i.text for i in _]


def section_judge_page(source):
    """Get the main section and clean empty paragraphs.
    Returns a bs4 tag object.
    """
    soup = BeautifulSoup(source, 'html.parser')
    main = soup.find(id='content_wrapper')
    for i in main.find_all('p'):
        if i.text == '\n' or len(i.text) == 0:
            i.extract()
    return main


def get_generic_section_text(src, section_title):
    """Find text in a section. Returns a list of tags.
    """
    section_text = []
    tag = src.find(string=section_title).parent
    while True:
        try: # avoids NoneType errors
            if tag.find_next_sibling(['p', 'h2']).name == 'p':
                tag = tag.find_next_sibling(['p', 'h2'])
                section_text.append(tag)
            else:
                break
        except AttributeError:
            break
    return section_text


def get_court(court_string):
    """Find the court(s) in which the judge presides.
    """
    return([s for s in court_string.stripped_strings][0])
    

def parse_judge_page(source):
    """Parse the judge detail page
    """
    outdict = {}
    page = section_judge_page(source)
    sections = [h2.text for h2 in page.find_all('h2')]

    # Get the court
    _ = get_generic_section_text(page, re.compile('Hon.'))
    outdict['court'] = [get_court(court) for court in _]

    # Parse the other sections
    for section in sections: # ignore the first part
        if 'Hon.' not in section:
            _ = get_generic_section_text(page, section)
            outdict[section] = [t.text for t in _]
        else:
            pass

    return outdict


# Try to load judges from the existing judges file
try:
    with open('judges.json', 'r') as f:
        JUDGES = json.load(f)
except:
    JUDGES = {}
print(JUDGES.keys())

# element = WebDriverWait(browser, 10).until(
                # EC.presence_of_element_located((By.ID, "column1_A630")))

# # For each letter in the alphabet, click on the link
for letter in list(string.ascii_uppercase):
    # Start the browser
    browser = webdriver.Firefox()
    browser.implicitly_wait(60)
    browser.get("https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory")
    pagejudges = scrape_alphabet_list(browser, letter)

    # TODO: fail gracefully by quitting and restarting
    # maybe pop judges so that if one fails it'll go again
    for judge in pagejudges:
        if judge not in JUDGES.keys():
            try:
                judge_url = browser.find_element_by_link_text(judge).get_attribute('href')
                # Append the judge's name +  url for the judge
                JUDGES[judge] = {'judge url': judge_url}
                time.sleep(10)

                browser.find_element_by_link_text(judge).click()
                judge_info = parse_judge_page(browser.page_source)

                # Update judge dict with all sections
                JUDGES[judge].update(judge_info)
                time.sleep(15)
                browser.back()
                print(judge + " detail page scraped")
            except:
                browser.quit()
                browser = webdriver.Firefox()
                browser.implicitly_wait(60)
                browser.get("https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory")
                browser.find_element_by_link_text(letter).click()
                browser.find_element_by_link_text(judge).click()
                judge_info = parse_judge_page(browser.page_source)

                # Update judge dict with all sections
                JUDGES[judge].update(judge_info)
                time.sleep(15)
                browser.back()
                print(judge + " detail page scraped")
        else:
            pass

    browser.quit()

with open('judges.json', 'w') as f:
    f.write(json.dumps(JUDGES))
