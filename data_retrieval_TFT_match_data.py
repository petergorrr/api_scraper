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

# Create directory for match data if it does not exist
match_data_dir = f"TFT_summoners_match_data_{region}"
if not os.path.isdir(match_data_dir):
    os.mkdir(match_data_dir)
else:
    print("The match folder already exists.")

# Process each JSON file containing match IDs
for path in pathlib.Path(f"TFT_match_id_{region}").iterdir():
    with open(path, "r", encoding="utf-8") as current_file:
        data = json.load(current_file)

        path_base = os.path.basename(path)
        puuid = os.path.splitext(path_base)[0]

        counter = 1

        for match_id in data:
            match_folder_path = f"{match_data_dir}/matches_{puuid}"
            if not os.path.isdir(match_folder_path):
                os.mkdir(match_folder_path)
            else:
                print("The match folder already exists.")

            start_time = time.time()

            # URL Creation
            URL = f"https://{url_region}.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={APIKey}"

            try:
                # Request URL
                response = requests.get(URL)

                # Get JSON of the data in the URL
                responseJSON = response.json()

                # Write the data into a JSON file
                with open(f"{match_folder_path}/{match_id}_match.json", "w", encoding='utf-8') as f:
                    json.dump(responseJSON, f, indent=4)

                print(f"The number of match id generated for this puuid:{counter}")
                counter += 1
                print("--- %s seconds ---" % (time.time() - start_time))

            except Exception as e:
                print(e)

            time.sleep(0.8)
