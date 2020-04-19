# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:21:37 2020

@author: ishat
"""

#Declerations of global variables 

from Phidget22.Phidget import*
from Phidget22.Devices.Accelerometer import*
import time
import numpy as np
import matplotlib.pyplot as plt

x=[]  #temporary vector to fill in phidget input for acceleration
t=[]  #temporary vector to fill in phidget input for time 
corrected_acc=[]  #corrected vector removing duplicate acceleration
corrected_dt=[]  #corected vector removing duplicate times
run_time=3  #runtime for experiment

#acceleration change event
def onaccelerationchange(self,acceleration,timestamp):
    global x
    global t
    for i in acceleration:
        x.append(acceleration)
        t.append(timestamp)
        
#channel opener and closer 
def main():    
    ch= Accelerometer()
    ch.setDeviceSerialNumber(372295)
    ch.setOnAccelerationChangeHandler(onaccelerationchange)
    
    ch.openWaitForAttachment(1000)
    time.sleep(run_time)
    ch.close()
    
#array manipulation of acceleration data
def list_to_arr():
    
    global finarr
    acc=Vector_correction(x,t)
    accarr=np.array(acc.acceleration_corr())
    dtarr=np.array(acc.timestamp_corr())
    finarr=np.column_stack((accarr,dtarr)) #combines both the arrays into one
    print(finarr)

#subtracts gravity from the inserted values
def gravity_correction(inarr):
    global acceleration_array
    ax=np.reshape(inarr[:,0],(12,1))
    ay=np.reshape(inarr[:,1],(12,1))
    az=np.reshape(inarr[:,2]-1,(12,1))
    dt=np.reshape(inarr[:,3],(12,1))
    acceleration_array=np.hstack((ax,ay,az,dt))
    
   # acc_array=np.reshape(s,(12,4))
# this should have the option of putting this numpy arr into a csv file
#function to create plot for testing 
#plots will have x, y , z accelerations 

def plot_acceleration(inputarr):
    a0=inputarr[:,0]
    a1=inputarr[:,1]
    a2=inputarr[:,2]
    t=inputarr[:,3]
    plt.figure(figsize=(12,20))
    plt.subplot(411)    
    plt.plot(t,a2,'b', label='z axis acce')
    plt.legend()

    plt.subplot(412)
    plt.plot(t,a0,'y', label='x axis acce')
    plt.legend()
    plt.subplot(413)
    plt.plot(t,a1,'g', label='y axis acce')
    plt.legend()
    plt.subplot(414)
    plt.plot(t,a2,'b', label='z axis acce')
    plt.plot(t,a0,'y', label='x axis acce')
    plt.plot(t,a1,'g', label='y axis acce')
    plt.legend()
    plt.show()
#creating a class to have accelearation and time corrected with array createad 
class Vector_correction:
    
    def __init__(self,acc,dt):
        self.acc=acc
        self.dt=dt
        
        
    def acceleration_corr(self):
        global corrected_acc
        # Also possible to use list(set())
        for a in self.acc:
            if a not in corrected_acc:
                corrected_acc.append(a)
                
        return corrected_acc
    
    def timestamp_corr(self):
        
        global corrected_dt
    
        for b in self.dt:
            if b not in corrected_dt:
                corrected_dt.append(b)
               
        return corrected_dt

try:
    main()
    onaccelerationchange()
finally: 
    list_to_arr()
    gravity_correction(finarr)
    plot_acceleration(acceleration_array)
    