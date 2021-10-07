import serial
i=0
h=0
y=0

ser = serial.Serial('/dev/ttyUSB0',9600)
print('Connected to Arduino')
ser.flush()

while True:
    read_serial=ser.readline().decode('utf8')
    print(read_serial)
#    if i < 2 : 
#        h[i] =read_serial.split("x")
#    else :
#        y[i] = read_serial.split("x")
#    
#    print ("real: ",h[i])
#    print ("imaginer: ",y[i])