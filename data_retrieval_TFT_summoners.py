import requests
import pathlib
import os
import time
import json
import sys

region = sys.argv[1]
APIKey = sys.argv[2]

# Mapping of region name to API URL region
region_mapping = {
    "kr": "kr",
    "jp": "jp1",
    "br": "br1",
    "eune": "eun1",
    "euw": "euw1",
    "tr": "tr1",
    "lan": "la1",
    "las": "la2",
    "oce": "oc1",
    "ru": "ru",
    "na": "na"
}

# Determine URL region
url_region = region_mapping.get(region, region)

# Create directory for summoners data if it does not exist
summoners_data_dir = f"TFT_summoners_data_{region}"
if not os.path.isdir(summoners_data_dir):
    os.mkdir(summoners_data_dir)
else:
    print(f"The TFT summoner folder of region {region} already exists.")

# Store summoners in a set
summoners = set()

# Load summoners from JSON files
for path in pathlib.Path(f"summoners_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)
        for item in data:
            summoners.add(item['name'])
    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))

# Process each summoner
counter = 1
for name in summoners:
    start_time = time.time()

    # Create URL
    URL = f"https://{url_region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}?api_key={APIKey}"

    try:
        # Request URL
        response = requests.get(URL)
        responseJSON = response.json()

        # Write the data into a JSON file and store it under the folder created earlier
        with open(f"{summoners_data_dir}/summoner_{name}.json", "w", encoding='utf-8') as f:
            json.dump(responseJSON, f, indent=4)

        print(f"i:{counter}")
        counter += 1
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(0.8)

    except Exception as e:
        print(e)
