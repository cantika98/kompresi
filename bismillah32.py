from timeit import default_timer as timer
start = timer()
import numpy as np
import math
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
import serial
import psutil
import os
##from sklearn.metrics import mean_squared_error
#import sklearn.metrics as metrics

#PENGIRIMAN DATA#

rawData = []
imaginaryData = []
realData = []


ser = serial.Serial('/dev/ttyACM0',9600)
print('Connected to Arduino')
ser.flush()

while True:
    read_serial =ser.readline().decode('utf8')
    print (read_serial) 
    if "Raw: " in read_serial:
        rawData.append(float(read_serial.replace("Raw: ", "").strip("\n")))
        print (rawData)
        
    elif "Converted: " in read_serial:
        real, imag= read_serial.replace("Converted: ", "").strip("\n").split("x")
        realData.append(float(real))
        imaginaryData.append(float(imag))
        print(imaginaryData)
        print (realData)
    elif "A" in read_serial:
        break
    

arr_real = np.asarray(realData)
arr_imag = np.asarray(imaginaryData)
print ('Real: ' ,arr_real)
print ('imag: ' ,arr_imag)

#DICTIONARY DATA#

toeplitz = np.genfromtxt('t3229.txt', delimiter = ',')
   
#RECONSTRUCTION PROCESS#

A = toeplitz
N = 32

#pre requiment
compressed = []
compress = 29

for x in range(compress):
    unite = complex(arr_real[x], arr_imag[x])
    compressed = np.append (compressed, unite)
print('complex: ',compressed)

com_trans = compressed.reshape(29,1)

y = com_trans
r = y
x_pre = np.zeros(N,dtype = 'complex')
O = []
i= 0
t = 1

print('StOMP Reconstruction start...\n')

for i in range(N):

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
#    print(O)
    Ao = toeplitz[:,O]
    
    x1 = np.linalg.pinv (Ao)
#    print('x1: ',x1)
    tilda = (x1.dot (y)).T
#    print('tilda: ', tilda)
    
    x2 = tilda.T
    
    r = y - (Ao.dot(x2))
    
    x_pre[O] = tilda
#    print('x_pre: ',x_pre)
    x_pre.size 

# print('result: ',x_pre)

inverse_fft = np.fft.ifft(x_pre)
print('ifft: ', inverse_fft)
real_num = inverse_fft.real
finaal = abs(real_num)
print(finaal)

plt_1 = plt.figure(figsize=(15,5))

plt.title("Original Signal of EEG")
plt.xlabel("Wavelenght (panjang data)")
plt.plot(rawData, marker ='o', label = 'Original')
plt.plot(finaal, marker = 'o', label = 'Reconstructed')
plt.legend()
plt.grid()

plt.show
end = timer()
print(end-start)
print("Processing time: ",end-start,'second')
mem =psutil.virtual_memory()
print(mem)
print("Rss:" ,psutil.Process(os.getpid()).memory_info().rss / 1024 **2)
print("Vms:" ,psutil.Process(os.getpid()).memory_info().vms / 1024 **2)
