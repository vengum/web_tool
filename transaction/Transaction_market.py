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
			"14": "Radish", "19": "Tomato", "16": "Spinach", "18": "Spinach-LP", "20": "Basil", "24": "Romaine", "22": "Mesculun"}
plant_skus_seed = {'Arugula': '11-211AR', 'Basil': '11-211BA', 'Beet':'11-211BE', 'Carrot':'11-211CT', 'Celery': '11-211CE', 'Cucumber':'11-211CU',\
			'Lettuce':'11-211SL', 'Mesclun':'11-211MS', 'Radish': '11-211RA', 'Romaine':'11-211LR', 'Spinach':'11-211SP'}
plant_skus_live = {'Tomato': '11-27003', 'Lettuce': '11-27001', 'Spinach':'11-27002'}
class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		Label(self, text='Email').grid(row=5)
		self.sel_email = tk.Entry(self)
		self.sel_email.grid(row=5, column=1)
		
		Label(self, text='Zipcode').grid(row=4)
		self.sel_zipcode = tk.Entry(self)
		self.sel_zipcode.grid(row=4, column=1)
		
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
		
		Label(self, text='Price').grid(row=6)
		self.sel_price = tk.Entry(self)
		self.sel_price.grid(row=6, column=1)
		
		Label(self, text='Plants(Seed Squares)').grid(row=7)
		self.sel_plants = tk.Entry(self)
		self.sel_plants.grid(row=7, column=1)
		
		Label(self, text='Plants(Live)').grid(row =8)
		self.sel_plant_live = tk.Entry(self)
		self.sel_plant_live.grid(row=8, column=1)
		
		
		self.gen = tk.Button(self, text='Generate', command=self.generate)
		self.gen.grid(row=9, column=1)
	
		self.quit = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
		self.quit.grid(row=9, column=2)
		
	def generate(self):
	
		day = self.sel_day.get()
		date = self.sel_yr.get()+'-'+self.mo.get()+'-'+'0'*(len(day)==1)+day
		
		try:
			datetime.datetime.strptime(date, '%Y-%m-%d')
		except ValueError:
			print(ValueError)
			messagebox.showerror('Error','Invalid date entered:\n'+date)
			return
		
		zipcode = str(self.sel_zipcode.get())
		email = str(self.sel_email.get())
		price = float(self.sel_price.get())
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
		req = requests.post('https://cryptic-falls-63527.herokuapp.com/transaction/new/', json={'zipcode': zipcode, 'email': email, 'date' : date, 'price': price, 'plants': myplants})
		response = req.json()
		if response is not None:
			messagebox.showerror('Transaction:', 'Transaction Successfully added')
		return root.destroy()
root = tk.Tk()
app = Application(master=root)
app.mainloop()