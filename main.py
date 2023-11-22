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

	sports_data, hostel_data, mess_data = extract(SERVER_IP, SERVER_USER, SERVER_PASSWORD)
	integrated_data = transform(sports_data, hostel_data, mess_data)
	load(integrated_data, SERVER_IP, SERVER_USER, SERVER_PASSWORD)

if __name__ == "__main__":
    main()