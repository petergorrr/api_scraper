'''
This script is used to scrape myMMR data of the summoners.
'''

import sys
import json
import time
import requests
import pathlib
import os

region = sys.argv[1]

# create a folder to store summoners' myMMR data later
os.mkdir(f"LoL_summoners_myMMR_{region}") if os.path.isdir(f"LoL_summoners_myMMR_{region}") is False else print(
    f"The myMMR summoner folder of region {region} already existed.")

# create a set to store the names of the summoners
summoners = set()

# Open JSON file by its directory path and add the name into the set
for path in pathlib.Path(f"LoL_summoners_name_{region}").iterdir():
    with open(path, "r", encoding="utf-8")as current_file:
        # read() returns string format , so we use loads() to convert json string document into python dictionary
        data = json.loads(current_file.read())

        # data is a list here , its elements are of type dictionary
        for item in data:
            summoners.add(item['name'])

print("\nThe total number of summoners in this region:", len(summoners), "\n")


counter = 1
for summoner in summoners:
    start_time = time.perf_counter()

    # URL creation
    URL = f"https://{region}.whatismymmr.com/api/v1/summoner?name={summoner}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    responseJSON = response.json()

    # dump the data into a file and store it under the folder created earlier
    with open(f"LoL_summoners_myMMR_{region}/myMMr_{summoner}.json", "w", encoding='utf-8')as f:
        json.dump(responseJSON, f, indent=4)

    print(f"i:{counter}")

    counter += 1

    end_time = time.perf_counter()

    print("--- %s seconds ---" % (end_time-start_time))

    time.sleep(0.5)
