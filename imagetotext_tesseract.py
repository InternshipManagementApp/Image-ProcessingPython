#!/usr/bin/env python

import cv2, numpy 
import pytesseract
from configparser import ConfigParser
import logging.config
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Anita\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' 

def convertColorToGrayScale(image): 
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
def convertGrayScaleToBinary(image): 
  return cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
  
def invertBlackAndWhite(image): #background is white and the foreground is black
  countWhite = numpy.sum(image > 0) #number of all pixel that are not black (255)
  countBlack = numpy.sum(image == 0) #number of all pixel that are black (0)
  if countBlack > countWhite:
    image = 255 - image
  return image

def getNumberFromImage(image, config): #tesseract
  #configuration: it will read only the specified language and for what to look for
  return pytesseract.image_to_string(image, lang=config['TESS_LANGUAGE'], 
    config='--psm ' + config['TESS_PAGESEGMEN'] + ' --oem ' + config['TESS_OCRENGINEMODE'] +' -c tessedit_char_whitelist=' + config['TESS_WHITELIST']) 

def main():
  #Read config.ini file
  config_object = ConfigParser()
  config_object.read(Path("config.ini"))
  config = config_object["DEFAULT"]

  logging.config.fileConfig('log_config.ini')
  logging.info('Starting .. ')
  logging.info('Stop')

  filePath = Path(config['OUTPUT_FILE'])
  if filePath.exists():
    filePath.unlink()
  file = open(config['OUTPUT_FILE'],"a")
  images = Path(config['FOLDER_NAME']).glob("*.jpg")
  for imagePath in images:
    image = cv2.imread(str(imagePath))
    
    #pre process tesseract
    image = convertColorToGrayScale(image)
    _, binaryImage = convertGrayScaleToBinary(image)
    binaryImage = invertBlackAndWhite(binaryImage)
    cv2.imshow(str(imagePath), binaryImage)
    cv2.waitKey(0)
    text = getNumberFromImage(image, config)
    file.write(str(imagePath) + " " +text)
    #print(text)

  logging.debug("Logging test...")  


if __name__ == '__main__':
    main()
