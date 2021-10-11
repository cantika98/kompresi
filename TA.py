#!/usr/bin/env python
# coding: utf-8

# # Compressed Signal Reconstruction Using StOMP for EEG Signal
# ### Cantika Puspa Karuniaputri - Telecommunication Engineering - School of Electrical Engineering
# 

# * Data aquisition using Neurosky MindWave Mobile 2 and Aruino Uno + HC-05 module
# * Data reconstruction using Raspberry Pi 
# * Successfully simulated on Matlab with compression ratio 75% with 64 data, MAPE approx. 10%

# In[2]:


import numpy as np
from numpy import linalg as LA
import scipy.io as sio
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import sys
np.set_printoptions(threshold=sys.maxsize)


# ## DATASET

# In[3]:


original = pd.read_excel ('eeg_data.xlsx') #original data
compressed = np.genfromtxt('compressed.txt', dtype = complex, delimiter = ',') #compressed signal
toeplitz = np.genfromtxt('BT4864.txt', dtype = None, delimiter = ',') #transfomation matrix
compressed


# ## Reconstruction Process

# In[14]:


A = toeplitz
data = range
N = 64

#pre requitment
y = compressed
r = y
x_pre = np.zeros(N, dtype = 'complex')
O = []
i = 0 #iteration
t = 15 #threshold

    
for i in range(2):

    # Compute the score of each atoms
    c = np.dot (A.T, r)
    absValues = np.abs (c)
        
    #noise level (standard deviation)
    sd =  np.linalg.norm(r,2)/ math.sqrt(N)
   
    #find the desired indices greater
    tsd = t*sd
    ind = np.where(absValues>=tsd)
    O = np.union1d(O, ind)
    vector = np.vectorize(int) #convert from float to int
    O = vector(O)
    Ao = toeplitz[:,O]
    
    x1 = np.linalg.pinv (Ao)
    tilda = (x1.dot (y)).T
    
    x2 = tilda.T
    
    r = y - (Ao.dot(x2))
    
    x_pre[O] = tilda
    final =x_pre[:, None]
    x_pre.size 

# print('result: ',x_pre)

inverse_fft = np.fft.ifft(x_pre)
index = [0 , 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5 , 4, 3, 2, 1]
idx = np.asarray(index)
final1 = inverse_fft[index]
real_num = final1.real
finaal = abs(real_num)
print(finaal)


