'''
This script is used to scrape myMMR data of the summoners.
'''

import sys
import json
import time
import requests
import pathlib
import os

def create_directory(region):
    """
    Creates a directory to store summoners' myMMR data if it does not already exist.
    """
    directory = f"LoL_summoners_myMMR_{region}"
    if not os.path.isdir(directory):
        os.mkdir(directory)
    else:
        print(f"The myMMR summoner folder for region {region} already exists.")

def load_summoner_names(region):
    """
    Loads summoner names from JSON files into a set.
    """
    summoners = set()
    for path in pathlib.Path(f"LoL_summoners_name_{region}").iterdir():
        with open(path, "r", encoding="utf-8") as current_file:
            data = json.load(current_file)
            for item in data:
                summoners.add(item['name'])
    return summoners

def fetch_mmr_data(summoner, region):
    """
    Fetches the myMMR data for a given summoner.
    """
    url = f"https://{region}.whatismymmr.com/api/v1/summoner?name={summoner}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {summoner}: {e}")
        return None

def save_mmr_data(summoner, region, data):
    """
    Saves the myMMR data to a JSON file.
    """
    filepath = f"LoL_summoners_myMMR_{region}/myMMr_{summoner}.json"
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <region>")
        return
    
    region = sys.argv[1]
    create_directory(region)
    summoners = load_summoner_names(region)
    
    print(f"\nThe total number of summoners in this region: {len(summoners)}\n")

    for counter, summoner in enumerate(summoners, start=1):
        start_time = time.perf_counter()
        data = fetch_mmr_data(summoner, region)
        if data:
            save_mmr_data(summoner, region, data)
        
        print(f"i: {counter}")
        end_time = time.perf_counter()
        print(f"--- {end_time - start_time:.2f} seconds ---")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
