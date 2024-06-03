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

# Create directory for match data if it does not exist
match_data_dir = f"LoL_summoners_match_data_{region}"
if not os.path.isdir(match_data_dir):
    os.mkdir(match_data_dir)
else:
    print(f"The match data folder for region {region} already exists.")

# Process each match ID file
for path in pathlib.Path(f"LoL_summoners_match_id_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)

    puuid = os.path.splitext(os.path.basename(path))[0]

    # Create directory for match if it does not exist
    match_dir = f"LoL_summoners_match_{region}/matches_{puuid}"
    if not os.path.isdir(match_dir):
        os.mkdir(match_dir)
    else:
        print("The match data folder already exists.")

    # Process each match ID
    counter = 1
    for match_id in data:
        start_time = time.time()

        # URL Creation
        URL = f"https://{url_region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={APIKey}"

        try:
            # Request URL
            response = requests.get(URL)
            responseJSON = response.json()

            with open(f"{match_dir}/{match_id}_match.json", "w", encoding='utf-8') as f:
                json.dump(responseJSON, f, indent=4)

            print(f"Number of matches generated for this puuid: {counter}")
            counter += 1
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(0.8)

        except Exception as e:
            print(e)
