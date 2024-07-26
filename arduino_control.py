import serial
import time



# Initialize the serial connection (make sure 'COM3' is the correct port)
ser = serial.Serial('COM3', 9600, timeout=1)  
time.sleep(2)  # Allow time for the connection to establish

while True:
    a = int(input("Enter 1 for 90°, 2 for 45°, 3 for 145°, any other number to exit: "))
    if a == 1:
        ser.write(b"90\n") 
    elif a == 2:
        ser.write(b"45\n") 
    elif a == 3:
        ser.write(b"75\n")
    else:
        break

ser.close()