import cv2
import serial
import sys

file = "Assets/Images/fff.jpg"
 
ser = serial.Serial('COM3', 57600, timeout = 1)

img = cv2.imread(file)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
row = gray_img.shape[0]
col = gray_img.shape[1]

print(row, col)

for i in range(row):
    for j in range(col):
        ser.write(str(gray_img[i][j]).encode() + b' ')
    ser.write(b'\r\n')