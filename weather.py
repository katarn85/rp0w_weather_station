import os
import json
import requests

def build_api_url(weather_api_root:str, station:str, gridpoints:str) -> str:

    api_url:str = weather_api_root + station + "/" + gridpoints + "/forecast"

    return api_url

def load_config(config_path:str) -> dict[str:str]:

    data:dict[str:str] = {}  # type: ignore

    if not config_path or not os.path.exists(config_path):
        raise ValueError('The provided file path is either empty or does not exist')

    if not os.path.isfile(config_path):
        raise TypeError('Provided path points to a directory, not a file')

    with open(config_path, 'r') as f:
        data = json.load(f)

    return data

def main():

    config_path:str = "config.json"
    api_params = load_config(config_path)
    api_url = build_api_url(**api_params)

    res = requests.get(api_url)
    weather_raw = {}

    if res.status_code == 200:
        weather_raw = json.loads(res.content)
    else:
        print(f"Failed to connect to '{api_url}'!")

    for period in weather_raw["properties"]["periods"]:
        print("{}, {}".format(period["name"], period["detailedForecast"]))

    return

if __name__ == '__main__':
    main()