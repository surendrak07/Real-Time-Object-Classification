import cv2
import serial
import time



ser = serial.Serial('COM6', 9600, timeout=1)  
time.sleep(2)

def classify_objects(contour,current):
    
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    vertices = len(approx)
    
    if area > 1000:
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if 0.85 <= aspect_ratio <= 1.2:
                return "Square"
            else:
                return "Rectangle"
        else:
            circularity = 4 * 3.1415 * area / (perimeter * perimeter)
            if circularity >= 0.7:
                return "Circle"
    return current

cap1 = cv2.VideoCapture(0)
link1 = "http://192.168.55.107:8080/video"
cap1.open(link1)
current_shape = None

while True:
    ret, frame = cap1.read()
    cv2.rectangle(frame,(200,200),(500,500),(255,0,0),2)
    small=frame[203:497,203:497]
    if not ret:
        break
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_shape = False 
    for contour in contours:
        shape = classify_objects(contour,current_shape)
        if shape != current_shape:
            current_shape = shape
            detected_shape = True
            print(shape)
            if shape== 'Circle':
                ser.write(b"25\n") 
            elif shape== 'Triangle':
                ser.write(b"50\n") 
            elif shape== 'Square':
                ser.write(b"75\n")
            elif shape== 'Rectangle':
                ser.write(b"100\n")
        cv2.putText(frame, current_shape, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Real-Time Object Classification', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
ser.close()
cap1.release()
cv2.destroyAllWindows()
