import requests
import csv
import os
import datetime
from datetime import *
import json
import pprint as p
from tkinter import messagebox
secret_key = "9lk453245poikj83b6923817cf885nlm"
concierge_data = {1: 'weather', 2: 'Light cold', 3: 'Very Cold', 4: 'Light Hot', 5: 'Very Hot'}
def generate():
		req = requests.post('https://cryptic-falls-63527.herokuapp.com/concierge/new/', json={'secret_key': secret_key, 'instruction': 'get_alerts'})
		response = req.json()
		reqdate = datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
		filename = 'concierge_data\\'+str(reqdate)+'.csv'
		concierge_alert = {}
		with open(filename, 'w') as csvfile:
			fieldnames = ['email'] + ['location'] + ['type'] + ['plant_name'] + ['start_date'] + ['end_date'] + ['stage']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
			writer.writeheader()
			for k, v in response.items():
				concierge_alert['email'] = k
				concierge_alert['location'] = response[k]['zipcode']
				for alert in response[k]['Alerts']:
					concierge_alert['plant_name'] = alert['plant_name']
					concierge_alert['stage'] = alert['plant_stage']
					concierge_alert['start_date'] = alert['start_date']
					concierge_alert['end_date'] = alert['end_date']
					concierge_alert['type'] = concierge_data.get(alert['concierge_id'])
					row = concierge_alert
					writer.writerow(row)
		os.startfile(filename)
if __name__ == '__main__':
	generate()
