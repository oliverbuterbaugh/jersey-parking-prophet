import requests
import csv
from datetime import datetime
import os
import time

while True:
    try:
        # public endpoint for live carpark data
        url = "https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json"

        response = requests.get(url)
        data = response.json()

        # reduce the timestamp to a more computer-friendly format
        timestamp = data['carparkData']['Timestamp']
        timestamp_datetime = datetime.strptime(timestamp, "This information was updated at %H:%M:%S on %A %d %B")
        formatted_timestamp = timestamp_datetime.strftime("%m-%d %H:%M:%S")


        filename = "carpark_data.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Carpark Code', 'Available Spaces', 'Carpark Open', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # write header if file does not exist
            if not file_exists:
                writer.writeheader()

            # write data
            for carpark in data['carparkData']['Jersey']['carpark']:
                carpark_code = carpark['code']
                available_spaces = carpark['spaces'] - carpark['numberOfUnusableSpaces']
                carpark_open = "True" if carpark['carparkOpen'] else "False"

                writer.writerow({
                    'Carpark Code': carpark_code,
                    'Available Spaces': available_spaces,
                    'Carpark Open': carpark_open,
                    'Timestamp': formatted_timestamp
                })

        print(f"Data appended to {filename} successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    # for running as an always on script, sleep for 5 min
    time.sleep(300)