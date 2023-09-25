"""
This script is used to retrieve summoners data.
"""

import os
import sys
import json
import time
import requests
import pathlib
from os import mkdir, path

region = sys.argv[1]
APIKey = sys.argv[2]

# URL region might be different from region name
if region == "kr":
    url_region = region
elif region == "ru":
    url_region = region
elif region == "na":
    url_region = region
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


# create a folder to store summoners' files later
if os.path.isdir(f"LoL_summoners_data_{region}") is False:
    os.mkdir(f"LoL_summoners_data_{region}")

else:
    print(f"The LoL summoner folder of region {region} already exists.")

# store summoners in a set
summoners = set()

# Open JSON file by its directory path
for path in pathlib.Path(f"LoL_summoners_names_{region}").iterdir():
    with open(path, "r", encoding="utf-8")as current_file:

        # read() returns string format , so we use loads() to convert json string document into python dictionary
        data = json.loads(current_file.read())

        # data is a list here , its elements are of type dictionary
        for item in data:
            summoners.add(item['name']) 

    print("File loaded:", path)

print("\nThe total number of summoners in this region:", len(summoners))

counter = 1

for summoner in summoners:
    start_time = time.perf_counter()

    # create URL
    URL = f"https://{url_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={APIKey}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    responseJSON = response.json()

    # write the data into a json file and store it under the folder created earlier
    with open(f"LoL_summoners_data_{region}/summoner_{summoner}.json", "w", encoding='utf-8') as f:
        json.dump(responseJSON, f, indent=4)

    print(f"i:{counter}")

    counter += 1

    end_time = time.perf_counter()

    print("--- %s seconds ---" % (end_time - start_time))

    time.sleep(0.8)
