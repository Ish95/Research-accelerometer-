# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 15:10:27 2020

@author: ishat
"""

from Phidget22.Phidget import*
from Phidget22.Devices.Accelerometer import*
import time

def onAccelerationChange(self,acceleration,timestamp):
    print("Acceleration:"+str(acceleration))
    print("Timestamp:"+str(timestamp))
    

def main():
    
    ch = Accelerometer()
    ch.setDeviceSerialNumber(372295)
    
    ch.setOnAccelerationChangeHandler(onAccelerationChange)

   
    ch.openWaitForAttachment(1000)
    
    time.sleep(1)
    
    ch.close()

main()

onAccelerationChange()


   
    

