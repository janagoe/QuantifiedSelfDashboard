
import configparser
import json
from oura_api_connector import OuraApiConnector

config = configparser.ConfigParser()
config.read("config.ini")
access_token = config["auth"].get('access-token')

conn = OuraApiConnector(access_token)

resp = conn.get_summary("sleep", start="2021-03-07")

print(json.dumps(resp, indent=4, sort_keys=True))
