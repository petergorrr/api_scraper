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

# Create directory for match timeline if it does not exist
match_timeline_dir = f"LoL_summoners_match_timeline_{region}"
if not os.path.isdir(match_timeline_dir):
    os.mkdir(match_timeline_dir)
else:
    print(f"The match timeline folder of region {region} already exists.")

# Process each match ID file
for path in pathlib.Path(f"LoL_summoners_puuid_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)

    puuid = os.path.splitext(os.path.basename(path))[0]

    # Process each match ID
    counter = 1
    for match_id in data:
        match_folder = f"LoL_summoners_match_timeline_{region}/matches_{puuid}"
        if not os.path.isdir(match_folder):
            os.mkdir(match_folder)
        else:
            print("The match folder for this puuid has already existed.")

        start_time = time.time()

        # URL Creation
        URL = f"https://{url_region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={APIKey}"

        try:
            # Request URL
            response = requests.get(URL)
            responseJSON = response.json()

            with open(f"{match_folder}/{match_id}_timeline.json", "w", encoding='utf-8') as f:
                json.dump(responseJSON, f, indent=4)

            print(f"i:{counter}")
            counter += 1
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(0.8)

        except Exception as e:
            print(e)
