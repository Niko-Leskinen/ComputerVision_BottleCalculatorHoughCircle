# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:47:01 2020

@author: Niko Leskinen
"""

import cv2
import numpy as np
import easygui
import sys

"""
 This function allows the user to fetch the image
from their computer with the help of file browser pop-up.
The fetched image is also processed inside this function. 
The function returns normal image and blurred grayscale image.
"""
def getImage():
    img = cv2.imread(easygui.fileopenbox(), cv2.IMREAD_COLOR)
    if img is None:
        sys.exit()
    # Grayscale conversation
    imgGr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur image to remove noise
    imgGrBlur = cv2.blur(imgGr, (5, 5))
    
    return img, imgGrBlur

"""
 This function is used to detect bottles, calculate the amount of bottles 
and draw circles around the bottles using the Hough transform found in
OpenCV-Python library. This function returns image with drawn circles and
also the amount of identified bottles.
"""
def detectBottles():
    img, imgGrBlur = getImage()
    bottlesAmount = 0;
    bottles = cv2.HoughCircles(imgGrBlur, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                                    param2 = 30, minRadius = 2, maxRadius = 22)
    
    # Draw circles on detected bottle tops
    if bottles is not None: 
        
        bottles = np.uint16(np.around(bottles)) 
  
        for i in bottles[0, :]:
            bottlesAmount = bottlesAmount + 1;
            a, b, r = i[0], i[1], i[2] 
  
            # Draw a circle on the identified bottle top
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
            
    return img, bottlesAmount

# This function starts the program.
def start():
    img, bottlesAmount = detectBottles()
    cv2.imshow("Detected bottles in crate: " + str(bottlesAmount), img)
    cv2.waitKey(0)
    # Continue the program until user closes the file browser window
    start()

start()