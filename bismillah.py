import serial

rawData = []
imaginary = []
real = []

ser = serial.Serial('/dev/ttyUSB1',9600)
print('Connected to Arduino')
ser.flush()

while True:
    read_serial=ser.readline().decode('utf8')
    for s in read_serial.splitlines():
        for t in read_serial.split():
                try:
                    rawData.append(float(t))
                except ValueError:
                    pass
                else:
                    if "x" in read_serial:
                        imaginary.append(float(read_serial.replace('x','')))
                    else:
                        real.append(float(read_serial))
                        print(real)     
