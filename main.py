from extract import *
from transform2 import *
from load2 import *

import mysql.connector
import json
import pandas as pd

SERVER_IP = '192.168.32.187'
SERVER_USER = 'root'
SERVER_PASSWORD = 'vhavle'

def main():

	with open('data_sources_config.json', 'r') as file:
		data_config = json.load(file)

	sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs = extract(SERVER_IP, SERVER_USER, SERVER_PASSWORD)
	integrated_df = transform(sports_dfs, hostel_dfs, mess_dfs, admin_dfs, access_dfs)
	load(integrated_df, SERVER_IP, SERVER_USER, SERVER_PASSWORD)

if __name__ == "__main__":
    main()