import glob
import json
import re
import sys
import time
import os
import requests
import pathlib

def get_server_region(region):
    if region in ["kr", "jp"]:
        return "asia"
    elif region in ["br", "lan", "las", "na"]:
        return "americas"
    elif region in ["eune", "euw", "ru", "oce", "tr"]:
        return "europe"
    return None

def get_url_region(region):
    region_mapping = {
        "kr": "kr",
        "ru": "ru",
        "na": "na",
        "jp": "jp1",
        "br": "br1",
        "eune": "eun1",
        "euw": "euw1",
        "tr": "tr1",
        "lan": "la1",
        "las": "la2",
        "oce": "oc1"
    }
    return region_mapping.get(region, None)

def load_summoner_names(region):
    summoners_name = set()
    for path in pathlib.Path(f"LOL_summoners_names_{region}").iterdir():
        with open(path, "r", encoding="utf-8") as current_file:
            data = json.load(current_file)
            for item in data:
                summoners_name.add(item['name'])
    return summoners_name

def fetch_summoner_puuids(summoners_name, url_region, APIKey):
    summoners_puuid = set()
    for name in summoners_name:
        URL = f"https://{url_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={APIKey}"
        try:
            response = requests.get(URL)
            responseJSON = response.json()
            summoners_puuid.add(responseJSON['puuid'])
        except Exception as e:
            print(f"Error fetching PUUID for {name}: {e}")
    return summoners_puuid

def fetch_match_ids(summoners_puuid, server_region, APIKey):
    summoners_match_id = []
    for puuid in summoners_puuid:
        URL = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={APIKey}"
        try:
            response = requests.get(URL)
            summoners_match_id.append(response.json())
        except Exception as e:
            print(f"Error fetching match IDs for PUUID {puuid}: {e}")
    return summoners_match_id

def fetch_match_data(summoners_match_id, server_region, APIKey):
    i = 1
    for match_id in summoners_match_id:
        for item in match_id:
            URL_match_data = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/{item}?api_key={APIKey}"
            URL_timeline = f"https://{server_region}.api.riotgames.com/lol/match/v5/matches/{item}/timeline?api_key={APIKey}"
            try:
                response_match_data = requests.get(URL_match_data)
                response_timeline = requests.get(URL_timeline)
                responseJSON_match_data = response_match_data.json()
                responseJSON_timeline = response_timeline.json()
                print(f"i: {i}")
                i += 1
            except Exception as e:
                print(f"Error fetching match data for match ID {item}: {e}")
            time.sleep(1.0)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <region> <APIKey>")
        return
    
    region = sys.argv[1]
    APIKey = sys.argv[2]

    server_region = get_server_region(region)
    url_region = get_url_region(region)

    if server_region is None or url_region is None:
        print("Invalid region specified.")
        return

    start_time = time.time()
    summoners_name = load_summoner_names(region)
    summoners_puuid = fetch_summoner_puuids(summoners_name, url_region, APIKey)

    print(f"Time taken to generate PUUID: {time.time() - start_time} seconds")
    print(f"Number of PUUIDs: {len(summoners_puuid)}")

    summoners_match_id = fetch_match_ids(summoners_puuid, server_region, APIKey)
    print(f"Time taken after finish generating match IDs: {time.time() - start_time} seconds")

    fetch_match_data(summoners_match_id, server_region, APIKey)
    print(f"Time taken to request 100 match data each for 1 summoner: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()
