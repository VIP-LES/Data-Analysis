# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:50:25 2019

@author: Richard
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

def get_sec(time): #helper function to convert serial output time string into int, just for testing convenience
    """Get Seconds from time."""
    time = str(time)[2:-1]
    h, m, s = str(time).split(':')
    ts = int(h) * 3600 + int(m) * 60 + float(s)
    return ts

class Data_Analysis:
    def __init__(self,logname,testing=False):
        if testing: #if you've made an output file by cping from the arduino serial output
            with open("Logs/" + str(logname)) as f:
                self.sensor_data=np.loadtxt((x.replace('->',',') for x in f),delimiter= ",",skiprows=1,converters = {0:get_sec}) #machine readability               
        else: #if you have a normal output file
            self.sensor_data = np.loadtxt("Logs/" + str(logname),delimiter = ",",skiprows = 1) #data, all floats (or ints)
        with open("Logs/" + str(logname)) as f: #getting column keys
                l1 = f.readline() 
                l1tags = l1.split(': ') #get rid of the leading junk, works the same for test or not, since ": " always follows "SENSOR SQUAD"
                l1list = l1tags[1].split() #get a list of useful stuff
                self.keys = {} 
                if testing == True:
                    self.keys[0] = 'computer_time'
                    for i in range(len(l1list)):
                        self.keys[l1list[i]] = i+1 #make a set of keys for easy access later
                else: 
                    for i in range(len(l1list)):
                        self.keys[l1list[i]] = i #make a set of keys for easy access later
        print(self.keys)
        
    def plot_2d_sensors(self,key_list): #given a set of data type names, generates plots comparing the two
        fig,ax = plt.subplots()
        ax.plot(self.sensor_data[:,self.keys[key_list[0]]],self.sensor_data[:,self.keys[key_list[1]]])
        ax.set_title("Plot of variables " + key_list[0] + " and " + key_list[1])
        ax.set_xlabel(key_list[0])
        ax.set_ylabel(key_list[1])
        return None
        
        
        
        
        
Test = Data_Analysis("SensorSerialLogSample.txt",testing=True)
Test.plot_2d_sensors(['time','geigercount'])
Test.plot_2d_sensors(['time','temp'])
Test.plot_2d_sensors(['time','humidity'])