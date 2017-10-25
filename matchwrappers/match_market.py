import requests
import csv
import os
import datetime
import tkinter as tk
import json
from tkinter import messagebox
from tkinter import Label
import pprint as p

plant_ids = {"1": "Arugula", "3": "Beet", "5": "Carrot", "7": "Cucumber", "9": "Celery", "11": "Lettuce", "13": "Lettuce-LP", \
			"14": "Radish", "19": "Tomato", "16": "Spinach", "18": "Spinach-LP", "20": "Basil", "25": "Romaine", "22": "Mesculun"}
plant_skus_seed = {'Arugula': '11-211AR', 'Basil': '11-211BA', 'Beet':'11-211BE', 'Carrot':'11-211CT', 'Celery': '11-211CE', 'Cucumber':'11-211CU',\
			'Lettuce':'11-211SL', 'Mesclun':'11-211MS', 'Radish': '11-211RA', 'Romaine':'11-211LR', 'Spinach':'11-211SP', 'Kale': '11-211KA'}
plant_skus_live = {'Tomato': '11-27003', 'Lettuce': '11-27001', 'Spinach':'11-27002'}

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		Label(self, text='Region').grid(row=0)
		regionList = ('zipcode','south','texas','mountains','west-coast','north','central','florida','east')
		self.reg = tk.StringVar()
		self.reg.set(regionList[0])
		self.sel_reg = tk.OptionMenu(self, self.reg, *regionList)
		self.sel_reg.grid(row=0,column=1)
		
		Label(self, text='Month').grid(row=1)
		monthList = ('01','02','03','04','05','06','07','08','09','10','11','12')
		self.mo = tk.StringVar()
		self.mo.set(monthList[0])
		self.sel_month = tk.OptionMenu(self, self.mo, *monthList)
		self.sel_month.grid(row=1, column=1)
		
		Label(self, text='Day').grid(row=2)
		self.sel_day = tk.Entry(self)
		self.sel_day.grid(row=2, column=1)
		
		Label(self, text='Year').grid(row=3)
		self.sel_yr = tk.Entry(self)
		self.sel_yr.grid(row=3, column=1)
		
		Label(self, text='Zipcode(blank if region)').grid(row=4)
		self.sel_zip = tk.Entry(self)
		self.sel_zip.grid(row=4, column =1)
		
		Label(self, text='Plants(Seed Squares)').grid(row=5)
		self.sel_plants = tk.Entry(self)
		self.sel_plants.grid(row=5, column=1)
		
		Label(self, text='Plants(Live)').grid(row =6)
		self.sel_plant_live = tk.Entry(self)
		self.sel_plant_live.grid(row=6, column=1)
		
		
		self.gen = tk.Button(self, text='Match Next Viable Date', command=self.generate)
		self.gen.grid(row=8, column=1)
		
		self.gen_2 = tk.Button(self, text='Match Specified Date', command=self.generate_2)
		self.gen_2.grid(row=7, column=1)
		
		self.quit = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
		self.quit.grid(row=9, column=1)
	def generate_2(self):
		day = self.sel_day.get()
		mydate = self.sel_yr.get()+'-'+self.mo.get()+'-'+'0'*(len(day)==1)+day
		try:
			datetime.datetime.strptime(mydate, '%Y-%m-%d')
		except ValueError:
			print(ValueError)
			messagebox.showerror('Error','Invalid date entered:\n'+mydate)
			return
		zipcode = str(self.sel_zip.get())
		if len(zipcode) < 4: zipcode = '00000'
		plants_seeds = self.sel_plants.get()
		plants_live = self.sel_plant_live.get()
		plants_live = plants_live.split(', ')
		plants_seeds = plants_seeds.split(', ')
		myplants = []
		i = 0
		while i < len(plants_seeds):
			if plant_skus_seed.get(plants_seeds[i]): myplants.append(str(plant_skus_seed.get(plants_seeds[i])))
			i += 1
		i = 0
		while i <len(plants_live):
			if plant_skus_live.get(plants_live[i]): myplants.append(str(plant_skus_live.get(plants_live[i])))
			i+=1
		region = self.reg.get()
		reqdate = datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
		filename = 'data\\'+mydate+'__'+region+'____req'+reqdate+'.csv'
		#req = requests.post('http://localhost:5000/match/new/', json={'zipcode': zipcode, 'email': '%s@bulk.com'%(region), 'plant_date' : mydate, 'plants': myplants, 'viable_date': False})
		req = requests.post('https://cryptic-falls-63527.herokuapp.com/match/new/', json={'zipcode': zipcode, 'email': '%s@bulk.com'%(region), 'plant_date' : mydate, 'plants': myplants, 'viable_date': False})
		jsondata = req.json()
		#.............................................
		#Loading dummy plant ids:
		#.............................................
		plant_scores = {}
		with open(filename, 'w') as csvfile:
			fieldnames = ['location'] + ['date'] + ['name'] + ['sku'] + ['stage'] + ['score']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
			writer.writeheader()
			row = {}
			for key, value in jsondata.items():
				row['location'] = key
				i =0
				while i < len(jsondata[key]):
					for k, v in jsondata[key][i].items():
						row['sku'] = k
						for x, y in jsondata[key][i][k].items():
							if x == 'name': row['name'] = y
							elif x == 'date': row['date'] = y
							elif x == 'stage': row['stage'] = y
							elif x == 'score': row['score'] = y
						i += 1
					writer.writerow(row)
		os.startfile(filename)
	def generate(self):
		day = self.sel_day.get()
		mydate = self.sel_yr.get()+'-'+self.mo.get()+'-'+'0'*(len(day)==1)+day
		try:
			datetime.datetime.strptime(mydate, '%Y-%m-%d')
		except ValueError:
			print(ValueError)
			messagebox.showerror('Error','Invalid date entered:\n'+mydate)
			return
		zipcode = str(self.sel_zip.get())
		if len(zipcode) < 4: zipcode = '00000'
		plants_seeds = self.sel_plants.get()
		plants_live = self.sel_plant_live.get()
		plants_live = plants_live.split(', ')
		plants_seeds = plants_seeds.split(', ')
		myplants = []
		i = 0
		while i < len(plants_seeds):
			if plant_skus_seed.get(plants_seeds[i]): myplants.append(str(plant_skus_seed.get(plants_seeds[i])))
			i += 1
		i = 0
		while i <len(plants_live):
			if plant_skus_live.get(plants_live[i]): myplants.append(str(plant_skus_live.get(plants_live[i])))
			i+=1
		region = self.reg.get()
		reqdate = datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
		filename = 'data\\'+mydate+'__'+region+'____req'+reqdate+'.csv'
		#req = requests.post('http://localhost:5000/match/new/', json={'zipcode': zipcode, 'email': '%s@bulk.com'%(region), 'plant_date' : mydate, 'plants': myplants, 'viable_date': True})
		req = requests.post('https://cryptic-falls-63527.herokuapp.com/match/new/', json={'zipcode': zipcode, 'email': '%s@bulk.com'%(region), 'plant_date' : mydate, 'plants': myplants, 'viable_date': True})
		jsondata = req.json()
		p.pprint(jsondata)
		#.............................................
		#Loading dummy plant ids:
		#.............................................
		plant_scores = {}
		with open(filename, 'w') as csvfile:
			fieldnames = ['location'] + ['date'] + ['name'] + ['sku'] + ['stage'] + ['score']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
			writer.writeheader()
			row = {}
			for key, value in jsondata.items():
				row['location'] = key
				i =0
				while i < len(jsondata[key]):
					for k, v in jsondata[key][i].items():
						row['sku'] = k
						for x, y in jsondata[key][i][k].items():
							if x == 'name': row['name'] = y
							elif x == 'date': row['date'] = y
							elif x == 'stage': row['stage'] = y
							elif x == 'score': row['score'] = y
						i += 1
					writer.writerow(row)
		os.startfile(filename)
root = tk.Tk()
app = Application(master=root)
app.mainloop()