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