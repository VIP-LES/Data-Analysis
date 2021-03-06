# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:50:25 2019

@author: Richard
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import pynmea2

def get_sec(time): #helper function to convert serial output time string into int, just for testing convenience
    """Get Seconds from time."""
    time = str(time)[2:-1]
    h, m, s = str(time).split(':')
    ts = int(h) * 3600 + int(m) * 60 + float(s)
    return ts

class Data_Analysis:
    def __init__(self, serial_log=None,gps_log=None):
        self.serial_log = serial_log
        self.gps_log = gps_log
    
    def read_serial(self,testing=False):
        if testing: #if you've made an output file by cping from the arduino serial output
            with open("Logs/" + str(self.serial_log)) as f:
                self.sensor_data=np.loadtxt((x.replace('->',',') for x in f),delimiter= ",",skiprows=1,converters = {0:get_sec}) #machine readability               
        else: #if you have a normal output file
            self.sensor_data = np.loadtxt("Logs/" + str(self.serial_log),delimiter = ",",skiprows = 1) #data, all floats (or ints)
        with open("Logs/" + str(self.serial_log)) as f: #getting column keys
                l1 = f.readline() 
                l1tags = l1.split(': ') #get rid of the leading junk, works the same for test or not, since ": " always follows "SENSOR SQUAD"
                l1list = l1tags[1].split() #get a list of useful stuff
                self.serial_keys = {} 
                if testing == True:
                    self.serial_keys[0] = 'computer_time'
                    for i in range(len(l1list)):
                        self.serial_keys[l1list[i]] = i+1 #make a set of keys for easy access later
                else: 
                    for i in range(len(l1list)):
                        self.serial_keys[l1list[i]] = i #make a set of keys for easy access later
        
    def read_gps(self,testing=False):
        #reading GPS data into more useful format, requires pynmea2 package
        with open("Logs/" +str(self.gps_log)) as file:
            gps_data_unparsed = file.readlines()
        gps_data_parsed = []
        for i in range(len(gps_data_unparsed)):
            if i%2 == 1: #we only want GNGGA format
                try: # t-e out of invalid values
                    gps_data_parsed += [pynmea2.parse(gps_data_unparsed[i])]
                except:
                    pass #should probably make this do something
        
        
        #TODO: Adapt this stuff to the data format generated above
        #self.lat_lon = np.genfromtxt(gps_file, delimiter = ";", skip_header = 2, usecols = (3,4)) #reads latitude and longitude from gps
        #self.lat_lon = self.lat_lon[:-1:2,:] #skips every other line to remove weird decoder artifact
        #self.speed = np.genfromtxt(gps_file, delimiter = ";", skip_header = 2, usecols = (6)) #reads speed from grps in kmph
        #self.speed = self.speed[:-1:2] #skips every other line to remove artifact
        #gps_time = pd.read_csv(gps_file,parse_dates=[0],sep=';',header= 1,usecols = [2]) #reads time from gps
        #gps_time = gps_time.to_numpy(dtype = 'datetime64[s]')
        #gps_time = gps_time[::2] #skips every other line to remove artifacts
        #self.altitude = np.genfromtxt(gps_altfile, delimiter = ",", skip_header = 1, usecols = (9))[1:-10:2]
        #self.altitude = np.reshape(self.altitude,(self.altitude.shape[0],1))
    
    def plot_2d_sensors(self,key_list): #given a set of data type names, generates plots comparing the two
        fig,ax = plt.subplots()
        ax.plot(self.sensor_data[:,self.serial_keys[key_list[0]]],self.sensor_data[:,self.serial_keys[key_list[1]]])
        ax.set_title("Plot of variables " + key_list[0] + " and " + key_list[1])
        ax.set_xlabel(key_list[0])
        ax.set_ylabel(key_list[1])
        return None
    
        
        
        
Test = Data_Analysis(serial_log ="SensorSerialLogSample.txt",gps_log="gps_raw_4-19.txt")
#Test.read_serial(testing=True)
#Test.plot_2d_sensors(['time','geigercount'])
#Test.plot_2d_sensors(['time','temp'])
#Test.plot_2d_sensors(['time','humidity'])
Test.read_gps(testing=True)