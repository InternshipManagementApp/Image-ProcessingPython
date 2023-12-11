#!/usr/bin/env python
import numpy, cv2

def invertBlackAndWhite(image): #background is white and the foreground is black
  countWhite = numpy.sum(image > 0) #number of all pixel that are not black (255)
  countBlack = numpy.sum(image == 0) #number of all pixel that are black (0)
  if countBlack > countWhite:
    image = 255 - image
  return image

def dilate(image):
  kernel = numpy.ones((5,5),numpy.uint8)
  return cv2.dilate(image, kernel, iterations = 1)
    
def erode(image):
  kernel = numpy.ones((5,5),numpy.uint8)
  return cv2.erode(image, kernel, iterations = 1)
    
def opening(image):
  kernel = numpy.ones((5,5),numpy.uint8)
  return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)