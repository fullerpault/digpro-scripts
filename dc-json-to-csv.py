import json
import csv

def json_to_csv(json_file, csv_file):
    # Open the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Extract the "results" array from the JSON data
    results = data["results"]
    
    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write the headers dynamically based on keys present in any object
        headers = set()
        for item in results:
            headers.update(item.keys())
        writer.writerow(list(headers))
        
        # Write the data
        for item in results:
            row = [item.get(key, "") for key in headers]
            writer.writerow(row)

# Example usage
json_file = ''  # Replace with your JSON file path
csv_file = ''    # Replace with your desired CSV file path
json_to_csv(json_file, csv_file)