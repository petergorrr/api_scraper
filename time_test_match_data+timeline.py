
import glob
import json
import re
import sys
import time
import os
import requests
import pathlib

region = sys.argv[1]
APIKey = sys.argv[2]

if region == "kr" or region == "jp":
    server_region = "asia"
elif region == "br" or region == "lan" or region == "las" or region == "na":
    server_region = "americas"
elif region == "eune" or region == "euw" or region == "ru" or region == "oce" or region == "tr":
    server_region = "europe"


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


start_time = time.time()

# store summoners in a set
summoners_name = set()

for path in pathlib.Path(f"LOL_summoners_names_{region}").iterdir():
    current_file = open(path, "r", encoding="utf-8")
    data = json.loads(current_file.read())

    for item in data:
        summoners_name.add(item['name'])


# store summoners in a set
summoners_puuid = set()

counter = 1
for name in summoners_name:
    another_start_time = time.time()

    # create URL
    URL = f"https://{url_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={APIKey}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    responseJSON = response.json()

    try:
        summoners_puuid.add(responseJSON['puuid'])

    except Exception as e:
        continue


print("Time taken to generate puuid: %s seconds" % (time.time() - start_time))
print(len(summoners_puuid))

summoners_match_id = []

for puuid in summoners_puuid:
    another_start_time = time.time()

    # URL Creation
    URL = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={APIKey}"

    try:
        # request URL
        response = requests.get(URL)

    except Exception as e:
        print(e)

    # get JSON of the data in the URL
    summoners_match_id.append(response.json())

    print("--- %s seconds ---" % (time.time() - another_start_time))

    # time.sleep(1.0)

print("Time taken after finish generating match id: %s seconds" %
      (time.time() - another_start_time))

i = 1
for match_id in summoners_match_id:
    for item in match_id:
        another_start_time = time.time()

        # URL Creation
        URL_match_data = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/{item}?api_key={APIKey}"
        URL_timeline = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/{item}/timeline?api_key={APIKey}"

        try:
            # request URL
            response_match_data = requests.get(URL_match_data)
            response_timeline = requests.get(URL_timeline)

        except Exception as e:
            print(e)

        # get JSON of the data in the URL

        responseJSON_match_data = response_match_data.json()
        responseJSON_timeline = response_timeline.json()

        print(f"i:{i}")
        i = i+1

        print("--- %s seconds ---" % (time.time() - another_start_time))

        time.sleep(1.0)


print("Time taken to request 100 match data each for 1 summoner: %s seconds" %
      (time.time() - start_time))
