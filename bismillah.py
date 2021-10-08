import numpy as np
from numpy import linalg as LA
import scipy.io as sio
import scipy
import pandas as pd
import matplotlib.pylot as plt
import matplotlib.patches as mpatches
import math
import sys
np.set_printoptions(threshold=sys.maxsize)
import serial

#PENGIRIMAN DATA#

rawData = []
imaginaryData = []
realData = []

ser = serial.Serial('/dev/ttyUSB0',9600)
print('Connected to Arduino')
ser.flush()

while True:
    read_serial =ser.readline().decode('utf8')
    if "Raw: " in read_serial:
        rawData.append(float(read_serial.replace("Raw: ", "").strip("\n")))
        
    elif "Converted: " in read_serial:
        realValue, imagValue = read_serial.replace("Converted: ", "").strip("\n").split("x")
        realData.append(float(realValue))
        imaginaryData.append(float(imagValue))
        
    print (read_serial)        
    print (rawData)        
    print (imaginaryData)
    print (realData)
    
#DICTIONARY DATA#

#toeplitz = np.genfromtxt('BT4864.txt'), dtype = None, delimiter = ',')
#    
##RECONSTRUCTION PROCESS#
#
#A = toeplitz
#data = range
#N = 64
#
##pre requiment
#for x in range(N):
#    unite = comprex(realData[x], imaginaryData[x])
#    y = np.append (y, unite)
#
#r = y
#x_pre = np.zeros(N,dtype = 'complex')
#O = []
#i= 0
#t = 15
#
##SToMP
#for i in range(64):
#    #compute the score of each atoms
#    c = np.dot (A.T,r)
#    absValues = np.abs (c)
#    
#    #noise leve (standard deviation)
#    sd = LA.norm (r,2)/ math.sqrt(N)
#    
#    #find the desired indices greater
#    tsd = t*sd
#    ind = np.where(absValues>=tsd)
#    O = union1d(O, ind)
#    vector = np.vectorize (int)
#    O = vector (O)
#    
#    Ao = toeplitz[:,0]
#    x1 = np.linalg.inv (Ao.T.dot(Ao)).dot(Ao.T).dot(y)
#    r = y -A.dot(x_pre)
#    x_pre[O] = x1
#    
#final = x_pre
#inv_fft = np.fft.ifft(final)
#real_num = inv_fft.real
#    
#
