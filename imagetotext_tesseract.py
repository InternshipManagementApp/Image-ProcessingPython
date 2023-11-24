#!/usr/bin/env python

import cv2, numpy 
import pytesseract
import os
from configparser import ConfigParser
import logging.config
from pathlib import Path

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Anita\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' 

def convertColorToGrayScale(image): #color picture to grayscale
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
def convertGrayScaleToBinary(image): #grayscale picture to binary
  return cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
  
def invertBlackAndWhite(image): #background is white and the foreground is black
  countWhite = numpy.sum(image > 0) #number of all pixel that are not black (255)
  countBlack = numpy.sum(image == 0) #number of all pixel that are black (0)
  if countBlack > countWhite:
    image = 255 - image
  return image

def getNumberFromImage(image): #tesseract
  #configuration: it will read only the specified language and for what to look for
  return pytesseract.image_to_string(image, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789') 

def main():
  #Read config.ini file
  config_object = ConfigParser()
  config_object.read(Path("config.ini"))
  config = config_object["DEFAULT"]
  print(config['THIS_EXAMPLE'])

  #Get the password
  account = config_object["ACCOUNT"]
  print("Status is: ", account["status"])
  #logtest

  logging.config.fileConfig('log_config.ini')
  logging.info('Starting .. ')
  # logging.basicConfig(filename="log.txt", level=logging.DEBUG,format="%(asctime)s %(message)s")
  # todo: move to config
  logging.info('Stop')

  folderName = "ImagesClock"

  # TODO: from pathlib import Path -- check this out
  if os.path.exists("result.txt"):
    os.remove("result.txt")
  file = open("result.txt","a")
  for imageName in os.listdir(folderName):
    image = cv2.imread(os.path.join(folderName,imageName))
    
    #pre process tesseract
    image = convertColorToGrayScale(image)
    _, binaryImage = convertGrayScaleToBinary(image)
    binaryImage = invertBlackAndWhite(binaryImage)
    cv2.imshow(imageName, binaryImage)
    cv2.waitKey(0)
    text = getNumberFromImage(image)
    file.write(imageName + " " +text)
    #print(text)

  logging.debug("Logging test...")  


if __name__ == '__main__':
    main()
