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
  
def addNoise(image):
    mean = -10 #with what intensity does noise appear on the image on average
    stddev = 35 #how much noisy will be the image
    noise = numpy.zeros(image.shape, numpy.uint8) #noise map
    cv2.randn(noise, mean, stddev) #generate noise
    noisy_img = cv2.add(image, noise)
    return noisy_img
    
def addBrightness(image):
    alpha = 1.0  # original image weight
    beta = -120    # value of brightness
    bright_image = cv2.addWeighted(image, alpha, numpy.zeros(image.shape, image.dtype), 0, beta)
    return bright_image