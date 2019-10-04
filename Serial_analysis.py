# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:50:25 2019

@author: Richard
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

def get_sec(time):
    """Get Seconds from time."""
    time = str(time)[2:-1]
    h, m, s = str(time).split(':')
    ts = int(h) * 3600 + int(m) * 60 + float(s)
    return ts

class Data_Read:
    def __init__(self,logname,testing=False):
        if testing:
            with open("Logs/" + str(logname)) as f:
                self.data=np.loadtxt((x.replace('->',',') for x in f),delimiter= ",",skiprows=1,converters = {0:get_sec})               
        else:
            self.data = np.loadtxt("Logs/" + str(logname),delimiter = ",",skiprows = 1)
        with open("Logs/" + str(logname)) as f:
                l1 = f.readline()
                l1tags = l1.split(': ')
                l1list = l1tags[1].split()
                self.keys = {}
                for i in range(len(l1list)):
                    self.keys[i] = l1list[i]

        print(self.keys)
        print(self.data)
Data_Read("SensorSerialLogSample.txt",testing=True)