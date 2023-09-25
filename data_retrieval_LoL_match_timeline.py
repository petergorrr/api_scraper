
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

if os.path.isdir(f"LoL_summoners_match_timeline_{region}") is False:
    os.mkdir(f"LoL_summoners_match_timeline_{region}")

else:
    print(f"The match timeline folder of region {region} already exists.")


for path in pathlib.Path(f"LoL_summoners_puuid_{region}").iterdir():
    current_file = open(path, "r", encoding="utf-8")
    data = json.loads(current_file.read())

    path_base = os.path.basename(path)
    puuid = os.path.splitext(path_base)[0]

    counter = 1
    for match_id in data:
        if os.path.isdir(f"LoL_summoners_match_timeline_{region}/matches_{puuid}") is False:
            os.mkdir(f"LoL_summoners_match_timeline_{region}/matches_{puuid}")

        else:
            print("The match folder for this puuid has already existed.")

        start_time = time.time()

        # URL Creation
        URL = f"https://{url_region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={APIKey}"

        try:
            # request URL
            response = requests.get(URL)

        except Exception as e:
            print(e)

        # get JSON of the data in the URL
        responseJSON = response.json()

        with open(f"LoL_summoners_match_timeline_{region}/matches_{puuid}/{match_id}_timeline.json", "w", encoding='utf-8')as f:
            json.dump(responseJSON, f, indent=4)

        print(f"i:{counter}")

        counter += 1

        print("--- %s seconds ---" % (time.time() - start_time))

        time.sleep(0.8)
