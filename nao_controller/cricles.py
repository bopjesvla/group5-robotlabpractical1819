import cv2
from PIL import Image, ImageTk
import math
import numpy as np

image = cv2.imread("ballpic.png")

# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# image = Image.fromarray(image)
# image.show()

lower_green = np.array([36,100,100], dtype = np.uint8)
upper_green = np.array([86,255,255], dtype = np.uint8)

#convert to a hsv colorspace
hsvImage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

#Create a treshold mask
color_mask=cv2.inRange(hsvImage,lower_green,upper_green)

#apply the mask on the image
green_image = cv2.bitwise_and(image,image,mask=color_mask)

kernel=np.ones((9,9),np.uint8)
#Remove small objects
opening =cv2.morphologyEx(color_mask,cv2.MORPH_OPEN,kernel)
#Close small openings
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
#Apply a blur to smooth the edges
smoothed_mask = cv2.GaussianBlur(closing, (9,9),0)

#Apply our (smoothend and denoised) mask
#to our original image to get everything that is blue.
green_image = cv2.bitwise_and(image,image,mask=smoothed_mask)

#Get the grayscale image (last channel of the HSV image
gray_image = green_image[:,:,2]

#Use a hough transform to find circular objects in the image.
circles = cv2.HoughCircles(
    gray_image,             #Input image to perform the transformation on
    cv2.HOUGH_GRADIENT,     #Method of detection
    1,                      #Ignore this one
    50,                      #Min pixel dist between centers of detected circles
    param1=200,             #Ignore this one as well
    param2=20,              #Accumulator threshold: smaller = the more (false) circles
    minRadius=5,            #Minimum circle radius
    maxRadius=100)          #Maximum circle radius

if circles is not None:
    print(circles)
    for x, y, r in circles[0]:
        cv2.circle(image, (x, y), r, (255, 255, 0), 5)