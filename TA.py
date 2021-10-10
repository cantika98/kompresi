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

    
for i in range(64):

    # Compute the score of each atoms
    c = np.dot (A.T, r)
    absValues = np.abs (c)
        
    #noise level (standard deviation)
    sd = LA.norm(r,2) / math.sqrt(N)
   
    #find the desired indices greater
    tsd = t*sd
    ind = np.where(absValues>=tsd)      
    O = np.union1d(O, ind)
    vector = np.vectorize(int) #convert from float to int
    O = vector(O)
    

    Ao = toeplitz[:,O]
    #print(Ao)
    x1 = np.linalg.inv(Ao.T.dot(Ao)).dot(Ao.T).dot(y)
    r = y - A.dot(x_pre)
    x_pre[O] = x1 
    x_pre.size           
    
final = x_pre
inv_fft = np.fft.ifft(final)
real_num = inv_fft.real
    


# In[15]:


real_num


# In[16]:


plt_1 = plt.figure(figsize=(15, 5))

plt.title("Original Signal of EEG")
plt.xlabel("Wavelength (Panjang Data)")
plt.plot(original, marker = 'o', label='Original')
plt.plot(real_num, marker = 'o', label ='reconstructed')
plt.legend()
plt.grid()

plt.show


# In[ ]:




