import tkinter as tk
from tkinter import ttk
#import color
from random import randint
import random
import time
from pylsl import StreamInlet, resolve_stream
import csv
import threading
from datetime import datetime


# start the tkinter window
root = tk.Tk()
root.geometry("200x200")
root.title("testing")

#start eeg stream with pylsl
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

#upload images

left = tk.PhotoImage(file="left.png")
right = tk.PhotoImage(file="right.png")


complete = tk.PhotoImage(file="complete.png")
rest = tk.PhotoImage(file="rest.png")

label = tk.Label(root, image= None)
label.image1 = left
label.image2 = right
label.image3 = complete
label.place(x=0, y=0)

#time interval between classess appearing on the screen
initial_time_interval = 5000
time_interval = 12000

#trials
total_trials = 20
num_trials = 0
class_one_index = -1
class_two_index = -1

#appending samples in 2 separate lists
sample_list_1 = []
sample_list_2 = []

#channels for enobio headset
header = ['channel 1','channel 2','channel 3','channel 4','channel 5','channel 6','channel 7','channel 8'
,'channel 9','channel 10','channel 11','channel 12','channel 13','channel 14','channel 15','channel 16','channel 17'
,'channel 18','channel 19','output']

#recording them in a csv file for machine learning use
def create_csv(file_name, sample_list, output):
	with open(file_name, 'a', newline ='') as file:	
		writer = csv.DictWriter(file, fieldnames = header)
		for i in range(0, len(sample_list)):

			writer.writerow(
				{'channel 1' : sample_list[i][0],
					'channel 2': sample_list[i][1],
					'channel 3': sample_list[i][2],
					'channel 4': sample_list[i][3],	
					'channel 5': sample_list[i][4],	
					'channel 6': sample_list[i][5],
					'channel 7': sample_list[i][6],
					'channel 8': sample_list[i][7],
					'channel 9': sample_list[i][8],
					'channel 10': sample_list[i][9],
					'channel 11': sample_list[i][10],
					'channel 12': sample_list[i][11],
					'channel 13': sample_list[i][12],
					'channel 14': sample_list[i][13],
					'channel 15': sample_list[i][14],
					'channel 16': sample_list[i][15],
					'channel 17': sample_list[i][16],
					'channel 18': sample_list[i][17],
					'channel 19': sample_list[i][18],
					'output':output,
				}
				)


def show_collected_data():
	#print("class_one samples")
	#print(sample_list_1)
	create_csv("left_data_samples.csv", sample_list_1, "left")
		

	#print("class_two samples")
	#print(sample_list_2)
	create_csv("right_data_samples.csv", sample_list_2, "right")

  
  #collecting  10 seconds of data every time a class appears on the screen
def collect_samples(sample_list, class_name):
	var = len(sample_list) + 5000
	print(f'{class_name},lenght: {len(sample_list)},var: {var}',datetime.now().strftime("%H:%M:%S"))
	while len(sample_list) < var:
		sample, timestamp = inlet.pull_sample()
		sample_list.append(sample)
	print(f'{class_name},lenght: {len(sample_list)},var: {var}', datetime.now().strftime("%H:%M:%S"))


  """
  if 40 trials then 20 trials for each class:
  logic for that in class_displayed()
  """

def class_displayed(class_num):
		global class_one_index
		global class_two_index
		if class_num == 1 and class_one_index < (total_trials / 2):
			#print("test 1: is it class one?")
			class_one_index += 1
			#print("class_one_index ", class_one_index)
			fun = class_one
		
		if class_num == 1 and class_one_index == (total_trials / 2):
			print("test 3: class 1 complete")
			if class_two_index < (total_trials / 2):
				#print("test 5: class 1 complete, is class two's trials done?")
				class_two_index += 1
				#print("class_two_index ", class_two_index)
				fun = class_two
			if class_two_index == (total_trials / 2):
				#print("test 7: class 2 complete, inside the checker of class one, calling disp")
				fun = display	

		if class_num == 2 and class_two_index < (total_trials / 2):
			#print("test 2: is it class two?")
			class_two_index += 1
			#print("class_two_index ", class_two_index)
			fun = class_two

		if class_num == 2 and class_two_index == (total_trials / 2):
			#print("test 4: class 2 complete")
			if class_one_index < (total_trials / 2):
				#print("test 6: class 2 complete, is class one's trials done?")
				class_one_index += 1
				#print("class_one_index ", class_one_index)
				fun = class_one
			if class_one_index == (total_trials / 2):
				#print("test 8: class 1 complete, inside the checker of class two, calling disp")
				fun = display	

		return fun		

  #generating which class to appear and keeping counter on trials
def blank_canvas():
	global num_trials

	global total_trials
	
	if num_trials < total_trials:
		
		class_num_ptr = random.random()
		if class_num_ptr < 0.5:
			class_num = 1
			
		else:
			class_num = 2
				
		#print("class number ", class_num)
		fun = class_displayed(class_num)



	#	if class_one_index == (total_trials / 2) and class_two_index == (total_trials / 2):
	#		fun = display 	
			 	

		num_trials += 1
		root.after(time_interval, fun)
		label.configure(image = rest)
	else:
		display()	
    
    
    #training ends
def display():
	print(" training ends")
	label.configure(image = complete)
	show_collected_data()

	
	

#class one
def class_one():
    root.after(time_interval, blank_canvas)
    label.configure(image=left)
    #print(f'left', datetime.now().strftime("%H:%M:%S"))
    threading.Thread(target = collect_samples, args = (sample_list_1, 'left', )).start()
	

    
#class two    
def class_two():
    root.after(time_interval, blank_canvas)
    label.configure(image=right)
    #print(f'right', datetime.now().strftime("%H:%M:%S"))
    threading.Thread(target = collect_samples, args =(sample_list_2, 'right', )).start()
         
 

	  


def start_training():
	root.after(initial_time_interval, blank_canvas)


button1 = tk.Button(root, text ="Start", command = start_training)
button1.place(x = 450, y = 650)

button2 = tk.Button(root, text ="quit", command = root.quit)
button2.place(x = 500, y = 650)


root.mainloop()    
