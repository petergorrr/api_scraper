import requests
import pathlib
import os
import time
import json
import sys

region = sys.argv[1]
APIKey = sys.argv[2]

# Determine URL region
if region in ["kr", "jp"]:
    url_region = "asia"
elif region in ["br", "tr", "lan", "las", "na", "oce"]:
    url_region = "americas"
elif region in ["eune", "euw", "ru"]:
    url_region = "europe"

# Create directory for summoner match IDs if it does not exist
summoners_match_id_dir = f"LoL_summoners_match_id_{region}"
if not os.path.isdir(summoners_match_id_dir):
    os.mkdir(summoners_match_id_dir)
else:
    print(f"The LoL summoner folder of region {region} already exists.")

# Store summoners in a set
summoners = set()

# Load summoners from JSON files
for path in pathlib.Path(f"LoL_summoners_data_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)
        for item in data:
            summoners.add(item['name'])
    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))

# Process each summoner
counter = 1
for puuid in summoners:
    start_time = time.time()

    # URL Creation
    URL = f"https://{url_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={APIKey}"

    try:
        # Request URL
        response = requests.get(URL)

        # Get JSON of the data in the URL
        responseJSON = response.json()

        # Skip if no match IDs are returned
        if len(responseJSON) == 0:
            continue

        else:
            with open(f"LoL_match_id_{region}/puuid={puuid}.json", "w", encoding='utf-8') as f:
                json.dump(responseJSON, f, indent=4)

        print(f"i:{counter}")
        counter += 1
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(0.8)

    except Exception as e:
        print(e)
