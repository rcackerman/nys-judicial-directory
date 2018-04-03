# New York Court System Judicial Directory
Directory of trial court judges in New York

A scraper to collect judge names from [https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory](https://iapps.courts.state.ny.us/judicialdirectory/JudicialDirectory). Hopefully will also collect assignments and other information in the future.

If you want to help, please [fork](https://help.github.com/articles/fork-a-repo/) and [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)!

## Requirements

1. Python 3.x
2. [Selenium for Python](https://pypi.python.org/pypi/selenium) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
3. [Geckodriver](https://github.com/mozilla/geckodriver/releases) ([This Stack Overflow answer](https://stackoverflow.com/a/40208762/702383) has a good overview of how to install on Windows and Unix systems)
4. Write access on your computer and familiarity with how to use terminal or Command Prompt.

## To Run

You will need to download this repo. You can either [clone](https://help.github.com/articles/cloning-a-repository/) it onto your computer, or download as a zip file.

In a terminal or Command Prompt session, navigate to the folder and run `python scraper.py`.

## To Do

* Scrape individual judge pages
* Parse individual judge pages
