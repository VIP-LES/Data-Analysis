# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 15:51:07 2019

@author: Richard
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



class Analysis:
    def __init__(self,gc_file="geigerlog-2018-10-21.csv",gps_file = "gps_trimmed.csv",gps_altfile = "gps_trimmed.txt"):
        self.gc_data = np.genfromtxt(gc_file,delimiter=",",usecols = (1)) #reads geiger counter counts
        gc_time = pd.read_csv(gc_file,parse_dates=[0],infer_datetime_format=True,sep=',',header=None,usecols = [0]) #reads geiger counter time stamp
        self.lat_lon = np.genfromtxt(gps_file, delimiter = ";", skip_header = 2, usecols = (3,4)) #reads latitude and longitude from gps
        self.lat_lon = self.lat_lon[:-1:2,:] #skips every other line to remove weird decoder artifact
        self.speed = np.genfromtxt(gps_file, delimiter = ";", skip_header = 2, usecols = (6)) #reads speed from grps in kmph
        self.speed = self.speed[:-1:2] #skips every other line to remove artifact
        gps_time = pd.read_csv(gps_file,parse_dates=[0],sep=';',header= 1,usecols = [2]) #reads time from gps
        gps_time = gps_time.to_numpy(dtype = 'datetime64[s]')
        gps_time = gps_time[::2] #skips every other line to remove artifacts
        gc_time = gc_time.to_numpy(dtype = 'datetime64[s]')
        print(gc_time.shape)
        gc_time[:,0] = gc_time[:,0] - np.timedelta64(1,'h')
        print(gc_time.shape)
        print(gc_time)
        self.gc_time_full = gc_time
        self.gc_data_full = self.gc_data
        self.gc_data = self.gc_data[gc_time[:,0]<gps_time[-1]]
        gc_time = gc_time[gc_time[:]<gps_time[-1]]
        gc_time = np.reshape(gc_time,(gc_time.shape[0],1))
        self.gc_data = np.reshape(self.gc_data,(self.gc_data.shape[0],1))
        self.speed = np.reshape(self.speed,(self.speed.shape[0],1))
        self.gps_time = gps_time[:-1]
        self.gc_time = gc_time
        self.altitude = np.genfromtxt(gps_altfile, delimiter = ",", skip_header = 1, usecols = (9))[1:-10:2]
        self.altitude = np.reshape(self.altitude,(self.altitude.shape[0],1))
       

    
    def plot_cpm(self,):
        self.create_full_array()
        y = self.gc_data[:-1]
        x= self.cut_alt
        t = self.cut_gps_time
        tf = self.gc_time_full[:3300]
        yf = self.gc_data_full[:3300]
        fig, ax = plt.subplots(figsize=(20,5))
        ax.plot(x,y)
        fig, ax = plt.subplots(figsize=(20,5))
        ax.plot(t,y)
        fig, ax = plt.subplots(figsize=(20,5))
        ax.plot(t,x)
        fig, ax = plt.subplots(figsize=(20,5))
        ax.plot(tf,yf)
        
        
        
    def create_full_array(self):
        ind_gps = np.in1d(self.gps_time,self.gc_time)
        ind_gc = np.in1d(self.gc_time, self.gps_time)
        print(ind_gps.shape)
        self.cut_gps_time = self.gps_time[ind_gps]
        self.cut_lat_lon = self.lat_lon[ind_gps]
        self.cut_speed = self.speed[ind_gps]
        self.cut_alt = self.altitude[ind_gps]
        print(self.cut_gps_time.shape)
        print(self.cut_alt.shape)
test = Analysis()
test.plot_cpm()

