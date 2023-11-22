from extract import *
from transform2 import *
from load2 import *

import mysql.connector
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
SERVER_IP = os.getenv("IP")
SERVER_USER = os.getenv("USERNAME")
SERVER_PASSWORD = os.getenv("PASSWORD")

def main():

	with open('data_sources_config.json', 'r') as file:
		data_config = json.load(file)

	sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs = extract(SERVER_IP, SERVER_USER, SERVER_PASSWORD)
	integrated_df = transform(sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs)
	load(integrated_df, SERVER_IP, SERVER_USER, SERVER_PASSWORD)

if __name__ == "__main__":
    main()