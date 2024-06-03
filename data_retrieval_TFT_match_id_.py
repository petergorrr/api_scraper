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
    "kr": "asia",
    "jp": "asia",
    "br": "americas",
    "tr": "americas",
    "lan": "americas",
    "las": "americas",
    "na": "americas",
    "oce": "americas",
    "eune": "europe",
    "euw": "europe",
    "ru": "europe"
}

# Determine URL region
url_region = region_mapping.get(region, region)

# Create directory for match ID data if it does not exist
match_id_data_dir = f"TFT_summoners_match_id_{region}"
if not os.path.isdir(match_id_data_dir):
    os.mkdir(match_id_data_dir)
else:
    print(f"The TFT summoner folder of region {region} already exists.")

# Store summoners in a set
summoners = set()

# Load summoners from JSON files
for path in pathlib.Path(f"LoL_summoners_data_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.loads(current_file.read())
        for item in data:
            summoners.add(item['name'])
    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))

counter = 1

# Process each summoner
for puuid in summoners:
    start_time = time.time()

    # Create URL
    URL = f"https://{url_region}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}?api_key={APIKey}"

    try:
        # Request URL
        response = requests.get(URL)
        responseJSON = response.json()

        # Write the data into a JSON file and store it under the folder created earlier
        if responseJSON:
            with open(f"TFT_summoners_match_id_{region}/puuid={puuid}.json", "w", encoding='utf-8') as f:
                json.dump(responseJSON, f, indent=4)

        print(f"i:{counter}")
        counter += 1
        print("--- %s seconds ---" % (time.time() - start_time))

    except Exception as e:
        print(e)

    time.sleep(0.8)
