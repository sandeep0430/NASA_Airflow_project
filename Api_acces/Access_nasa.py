import requests
import csv

from datetime import datetime

# Define the API endpoint URL
api_url = 'https://api.nasa.gov/neo/rest/v1/neo/browse'

# Construct the API request with your API key
api_key = 'your_key'
params = {'api_key': api_key}

# Send the API request
response = requests.get(api_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Initialize list to store all data
    all_neo_data = []

    # Loop through the first 5 pages (20 items per page, for a total of 100 items)
    for page_number in range(5):
        params['page'] = page_number + 1  # Adjust the page number in the request

        # Send the API request for this page
        response = requests.get(api_url, params=params)

        # Parse the JSON response for this page
        page_data = response.json()

        # Extract relevant data fields from the response for this page
        for neo in page_data['near_earth_objects']:
            closest_approach_date_full = neo['close_approach_data'][0]['close_approach_date_full']
            closest_approach_date = datetime.strptime(closest_approach_date_full, '%Y-%b-%d %H:%M')

            estimated_diameter_km_max = neo['estimated_diameter']['kilometers']['estimated_diameter_max']
            velocity = neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']

            all_neo_data.append([
                neo['id'],
                neo['name'],
                neo['absolute_magnitude_h'],
                estimated_diameter_km_max,
                neo['is_potentially_hazardous_asteroid'],
                closest_approach_date.strftime('%Y-%m-%d %H:%M'),
                velocity,
            ])

    # Write the extracted data to a CSV file
    csv_filename = 'NASA.csv'
    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'name',
                         'magnitude', 'diameter',
                         'hazardous', 'closest_approach_date', 'velocity'])  # Write header row
        writer.writerows(all_neo_data)  # Write data rows
    print(f"Data has been extracted and saved to '{csv_filename}'")
else:
    print(f"Failed to retrieve data: HTTP status code {response.status_code}")
