"""Webscraping script to get permalinks from Primo ILS

This script takes a list of Primo search URLs from a CSV as input
and returns a list of Primo Permalinks to a CSV output file.
This uses Selenium to load the website into a headless browser, which
requires having the Chrome webdriver. See the Selenium documentation
for more information on usage:
https://www.selenium.dev/documentation/webdriver/

To create the Primo search URLs, use a spreadsheet program to concatenate
a search string of the item's bibnumber in quote and included in the search
string. The bibnumber used in the Ursus permalinks does not have the final
digit, but this is a check-digit so we can use the * wildcard in its place
and still find the correct item in Primo the vast majority of the time.

The search string will have three parts:
1. https://maine.primo.exlibrisgroup.com/discovery/search?query=any,contains,%22
2. bibnumber* (e.g. b1234567*)
3. %22&tab=LibraryCatalog&search_scope=MyInstitution&vid=01MAINE_INST:USM&offset=0

Concatenate those strings to get the Primo search URLs, which are then used
to locate the new AlmaIDs for each item. The AlmaID is the final
part of the permalinks.

In the Primo permalink before the AlmaID is a key that is calculated
based on the search parameters. Using the strings above, the key will
be "5j44tu". If you decide to use other search parameters you may
find a different key. As far as I can tell as long as you use a valid
key there are no problems with the final permalinks, which is why I have
hardcoded the key into the base_url variable.
"""

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import ChromiumOptions

# initialize the webdriver
options = ChromiumOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Function to get almaid from the webpage
def get_almaID(url):
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-recordid]")))
        almaID = element.get_attribute('data-recordid')
        return almaID, None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, str(e)

# Read input CSV file
input_csv = 'path/to/input/file.csv'
output_csv = 'path/to/output/file.csv'
base_url = "https://maine.primo.exlibrisgroup.com/permalink/01MAINE_INST/5j44tu/"

with open(input_csv, mode='r', newline='') as infile, open(output_csv, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['almaID', 'permalink', 'error']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()
    
    # Process each row
    for row in reader:
        url = row['primo_search_url']
        if not url:
            continue
        almaID, error = get_almaID(url)
        permalink = base_url + almaID if almaID else None
        row['almaID'] = almaID
        row['permalink'] = permalink
        row['error'] = error
        writer.writerow(row)

# Close the WebDriver
driver.quit()

print(f"Results have been written to {output_csv}")