"""
This script takes in puuid and retrieves match id
"""

import requests
import pathlib
import os
import time
import json
import sys

region = sys.argv[1]
APIKey = sys.argv[2]

# URL region might have a different name
if region == "kr" or region == "jp":
    url_region = "asia"
elif region == "br" or region == "tr" or region == "lan" or region == "las" or region == "na" or region == "oce":
    url_region = "americas"
elif region == "eune" or region == "euw" or region == "ru":
    url_region = "europe"

# create a folder to store summoners' files later
if os.path.isdir(f"TFT_summoners_match_id_{region}") is False:
    os.mkdir(f"TFT_summoners_match_id_{region}")

else:
    print(f"The TFT summoner folder of region {region} already exists.")


# store summoners in a set
summoners = set()

# Open JSON file by its directory path
for path in pathlib.Path(f"LoL_summoners_data_{region}").iterdir():
    with open(path, "r", encoding="utf-8")as current_file:
        data = json.loads(current_file.read())
        for item in data:
            summoners.add(item['name'])

    print("File loaded:", path)


print("\nThe total number of summoners in this region:", len(summoners))

counter = 1

for puuid in summoners:
    start_time = time.time()

    # URL Creation
    URL = f"https://{url_region}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}?api_key={APIKey}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    responseJSON = response.json()

    if len(responseJSON) == 0:
        continue

    else:
        with open(f"TFT_puuid_{region}/puuid={puuid}.json", "w", encoding='utf-8')as f:
            json.dump(responseJSON, f, indent=4)

    print(f"i:{counter}")
    counter += 1

    print("--- %s seconds ---" % (time.time() - start_time))

    time.sleep(0.8)
