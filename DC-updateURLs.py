import pandas as pd
import re

# Load the spreadsheets
dc_records = pd.read_excel('path/to/dc/batch/revise.xls')
primo_links_sheet = pd.read_excel('path/to/sheet/with/primo/links.xlsx')

# function to find and replace the href attribute
def replace_href(html_content, new_url):
    pattern = r'(href=")([^"]*)(")'
    replacement = rf'\1{new_url}\3'
    return re.sub(pattern, replacement, html_content)

# Define the columns
match_column = 'calc_url'  # Column to match
url_column = 'catalog_url'  # Column to pull updated URL from primo_links_sheet
target_column = 'ext_link'  # Column in dc_records where the href replacement should occur

# Create a dictionary for fast lookup
update_dict = primo_links_sheet.set_index(match_column)[url_column].to_dict()

# Update the target column in dc_records
def update_row(row):
    match_value = row[match_column]
    if match_value in update_dict:
        return update_dict[match_value]
    return row[target_column]

# Apply the replacement
dc_records[target_column] = dc_records.apply(lambda row: update_row(row), axis=1)

# Save the updated dc_mecollection
dc_records.to_excel('updated-spreadsheet.xlsx', index=False)
