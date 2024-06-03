import os
import sys
import json
import time
import requests
import pathlib

region = sys.argv[1]
APIKey = sys.argv[2]

# Mapping of region name to API URL region
region_mapping = {
    "kr": "kr",
    "ru": "ru",
    "na": "na",
    "jp": "jp1",
    "br": "br1",
    "eune": "eun1",
    "euw": "euw1",
    "tr": "tr1",
    "lan": "la1",
    "las": "la2",
    "oce": "oc1"
}

# Determine URL region
url_region = region_mapping.get(region, region)

# Create directory for summoners data if it does not exist
summoners_data_dir = f"LoL_summoners_data_{region}"
if not os.path.isdir(summoners_data_dir):
    os.mkdir(summoners_data_dir)
else:
    print(f"The LoL summoner folder of region {region} already exists.")

# Store summoners in a set
summoners = set()

# Load summoners from JSON files
for path in pathlib.Path(f"LoL_summoners_names_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)
        for item in data:
            summoners.add(item['name'])
    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))

# Process each summoner
counter = 1
for summoner in summoners:
    start_time = time.perf_counter()

    # Create URL
    URL = f"https://{url_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={APIKey}"

    try:
        # Request URL
        response = requests.get(URL)
        responseJSON = response.json()

        # Write the data into a JSON file and store it under the folder created earlier
        with open(f"{summoners_data_dir}/summoner_{summoner}.json", "w", encoding='utf-8') as f:
            json.dump(responseJSON, f, indent=4)

        print(f"i:{counter}")
        counter += 1
        end_time = time.perf_counter()
        print("--- %s seconds ---" % (end_time - start_time))
        time.sleep(0.8)

    except Exception as e:
        print(e)
