"""
This script is used to retrieve summoners data.
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
if region == "kr":
    url_region = "kr"
elif region == "jp":
    url_region = "jp1"
elif region == "br":
    url_region = "br1"
elif region == "eune":
    url_region = "eun1"
elif region == "euw":
    url_region = "euw1"
elif region == "tr":
    url_region = "tr1"
elif region == "lan":
    url_region = "la1"
elif region == "las":
    url_region = "la2"
elif region == "oce":
    url_region = "oc1"
elif region == "ru":
    url_region = "ru"
elif region == "na":
    url_region = "na"

# create a folder to store summoners' files later
if os.path.isdir(f"TFT_summoners_data_{region}") is False:
    os.mkdir(f"TFT_summoners_data_{region}")

else:
    print(f"The TFT summoner folder of region {region} already exists.")


# store summoners in a set
summoners = set()

# Open JSON file by its directory path
for path in pathlib.Path(f"summoners_{region}").iterdir():
    current_file = open(path, "r", encoding="utf-8")
    data = json.loads(current_file.read())

    # add the names into the set
    for item in data:
        summoners.add(item['name'])

    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))


counter = 1
for name in summoners:
    start_time = time.time()

    # create URL
    URL = f"https://{url_region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}?api_key={APIKey}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    responseJSON = response.json()

    with open(f"TFT_summoners_data_{region}/summoner_{name}.json", "w", encoding='utf-8')as f:
        json.dump(responseJSON, f, indent=4)

    print(f"i:{counter}")

    counter += 1

    print("--- %s seconds ---" % (time.time() - start_time))

    time.sleep(0.8)
