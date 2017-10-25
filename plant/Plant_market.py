import requests
import csv
import os
import datetime
from datetime import *
import tkinter as tk
import json
from tkinter import messagebox
from tkinter import Label
from tkinter import *
import pprint as p
secret_key = "9lk453245poikj83b6923817cf885nlm"
class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		def_string = StringVar(self, value='None')
		def_int = StringVar(self, value='-1')
		Label(self, text='Command').grid(row=0)
		self.sel_name = tk.Entry(self)
		self.sel_name.grid(row=1, column=1)
		
		commandlist = ('Create', 'Modify')
		self.com = tk.StringVar()
		self.com.set(commandlist[0])
		self.sel_com = tk.OptionMenu(self, self.com, *commandlist)
		self.sel_com.grid(row=0,column=1)
		
		self.query = tk.Button(self, text='Query', command=self.query)
		self.query.grid(row=0, column=2)
		
		stageList = ('SS-1','SS-2','LP', 'H')
		self.reg = tk.StringVar()
		self.reg.set(stageList[0])
		self.sel_stage = tk.OptionMenu(self, self.reg, *stageList)
		self.sel_stage.grid(row=1,column=2)
		
		Label(self, text='Name').grid(row=1)
		Label(self, text='SKU || Sun min').grid(row=2)
		self.sel_sun = tk.Entry(self)
		self.sel_sun.insert(END, '-1')
		self.sel_sun.grid(row=2, column=2)
		self.sel_sku = tk.Entry(self)
		self.sel_sku.insert(END, 'None')
		self.sel_sku.grid(row=2, column=1)
		Label(self, text='Low').grid(row=3, column=1)
		Label(self, text='High').grid(row=3, column=2)
		
		
		Label(self, text='Day Range').grid(row=4)
		self.sel_day_low = tk.Entry(self)
		self.sel_day_low.insert(END, '-1')
		self.sel_day_high = tk.Entry(self)
		self.sel_day_high.insert(END, '-1')
		self.sel_day_low.grid(row=4, column =1)
		self.sel_day_high.grid(row=4, column=2)
		
		Label(self, text='Ideal Temp').grid(row=5)
		self.sel_ideal_low = tk.Entry(self,)
		self.sel_ideal_low.insert(END, '-1')
		self.sel_ideal_high = tk.Entry(self)
		self.sel_ideal_high.insert(END, '-1')
		self.sel_ideal_low.grid(row=5, column =1)
		self.sel_ideal_high.grid(row=5, column =2)
		
		Label(self, text='Tolerance Temp').grid(row=6)
		self.sel_tol_low = tk.Entry(self)
		self.sel_tol_low.insert(END, '-1')
		self.sel_tol_high = tk.Entry(self)
		self.sel_tol_high.insert(END, '-1')
		self.sel_tol_low.grid(row=6, column =1)
		self.sel_tol_high.grid(row=6, column=2)
		
		Label(self, text='Sun Range').grid(row=7)
		self.sel_sun_low = tk.Entry(self)
		self.sel_sun_low.insert(END, '-1')
		self.sel_sun_high = tk.Entry(self)
		self.sel_sun_high.insert(END, '-1')
		self.sel_sun_low.grid(row=7, column =1)
		self.sel_sun_high.grid(row=7, column=2)
		
		Label(self, text='PH Ideal').grid(row=8)
		self.sel_ph_low = tk.Entry(self)
		self.sel_ph_low.insert(END, '-1')
		self.sel_ph_high = tk.Entry(self)
		self.sel_ph_high.insert(END, '-1')
		self.sel_ph_low.grid(row=8, column =1)
		self.sel_ph_high.grid(row=8, column=2)
		
		Label(self, text='PH Tolerance').grid(row=9)
		self.sel_ph_tol_low = tk.Entry(self)
		self.sel_ph_tol_low.insert(END, '-1')
		self.sel_ph_tol_high = tk.Entry(self)
		self.sel_ph_tol_high.insert(END, '-1')
		self.sel_ph_tol_low.grid(row=9, column =1)
		self.sel_ph_tol_high.grid(row=9, column=2)
		
		Label(self, text='Night Temp').grid(row=10)
		self.sel_night_low = tk.Entry(self)
		self.sel_night_low.insert(END, '-1')
		self.sel_night_high = tk.Entry(self)
		self.sel_night_high.insert(END, '-1')
		self.sel_night_low.grid(row=10, column =1)
		self.sel_night_high.grid(row=10, column=2)
		
		self.gen = tk.Button(self, text='Generate', command=self.generate)
		self.gen.grid(row=11, column=1)
	
		self.quit = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
		self.quit.grid(row=11, column=2)
	def query(self):
		req = requests.get('https://cryptic-falls-63527.herokuapp.com/plant/plants/', json={'secret_key': secret_key})
		response = req.json()
		reqdate = datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
		filename = 'plant_data\\'+str(reqdate)+'.csv'
		plant_data = {}
		with open(filename, 'w') as csvfile:
			fieldnames = response[0].keys()
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
			writer.writeheader()
			i = 0
			while i < len(response):
				for k, v in response[i].items():
					plant_data[k]  = v
				row = plant_data
				writer.writerow(row)
				i += 1
		os.startfile(filename)
		return p.pprint(response)
	def generate(self):
		temp_ideal = [self.sel_ideal_low.get(), self.sel_ideal_high.get()]
		temp_tolerance = [self.sel_tol_low.get(), self.sel_tol_high.get()]
		night_range = [self.sel_night_low.get() if self.sel_night_low.get() else 0, self.sel_night_high.get() if self.sel_night_high.get() else 0]
		day_range = [int(self.sel_day_low.get()), int(self.sel_day_high.get())]
		ph_ideal = [self.sel_ph_low.get(), self.sel_ph_high.get()]
		ph_tol = [self.sel_ph_tol_low.get(), self.sel_ph_tol_high.get()]
		sun_range = [int(self.sel_sun_low.get()), int(self.sel_sun_high.get())]
		sun_min = int(self.sel_sun.get())
		sku =  self.sel_sku.get()
		stage = self.reg.get()
		name = self.sel_name.get()
		mycommand = self.com.get()

		req = requests.post('http://localhost:5000/plant/plants/', json={'name': name, 'stage': stage, 'sku' : sku, 'temp_ideal': temp_ideal, 'temp_tolerance': temp_tolerance, \
							'day_range': day_range, 'ph_ideal': ph_ideal, 'ph_tolerance': ph_tol, 'sun_minimum':  sun_min, 'sun_ideal': sun_range, 'night_temp': night_range,\
							'secret_key': secret_key, 'command': mycommand})
root = tk.Tk()
app = Application(master=root)
app.mainloop()