from extract import *
from transform import *
from load import *

import mysql.connector
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_IP = os.getenv("DB_IP")
SERVER_USER = os.getenv("DB_USERNAME")
SERVER_PASSWORD = os.getenv("DB_PASSWORD")

def main():

	print(SERVER_IP, SERVER_USER, SERVER_PASSWORD)
	with open('data_sources_config.json', 'r') as file:
		data_config = json.load(file)

	sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs = extract(SERVER_IP, SERVER_USER, SERVER_PASSWORD)
	integrated_dfs = transform(sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs)
	load(integrated_dfs, SERVER_IP, SERVER_USER, SERVER_PASSWORD)

if __name__ == "__main__":
    main()