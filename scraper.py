import string
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Start the browser
browser = webdriver.Firefox()

# For some reason javascript doesn't kick in right away
# so as a kludgey fix, just visit the site to initialize
browser.get("https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory")
print(browser.title)
print("\n\n\n")

JUDGES = []

browser.get("https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory")
# For each letter in the alphabet, click on the link
for letter in list(string.ascii_uppercase):
    print(letter)
    try:
        browser.find_element_by_link_text(letter).click()

        # Each alphabetized page has links to the judges, which we will record
        judges = browser.find_elements_by_xpath("//a[contains(@href, 'JUDGE_ID')]")
        for judge in judges:
            judge_name = judge.text
            judge_url = judge.get_attribute('href')

            # Append the judge's name and the url for the judge
            JUDGES.append({'judge name': judge_name, 'judge url': judge_url})
            print(judge_name)
    except:
        print(letter + "did not work")
        pass

browser.quit()

with open('judges.csv', 'w', newline='') as csvfile:
    fieldnames = ['judge name', 'judge url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for j in JUDGES:
        writer.writerow(j)
