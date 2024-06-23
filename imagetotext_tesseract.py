#!/usr/bin/env python

import cv2, numpy 
import pytesseract
from configparser import ConfigParser
import logging.config
from pathlib import Path 
import utils
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Anita\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' 

class ImageToText:
  def __init__ (self, image):
    self.image = image
    
  def preprocess(self):
    grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    _, binaryImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_OTSU)
    binaryImage = utils.invertBlackAndWhite(binaryImage)
    erodeImg = utils.erode(binaryImage)
    #dilateImg = utils.dilate(binaryImage)
    #openingImg = utils.opening(binaryImage)
    return erodeImg

  def getTheImage(self):
    return self.image
    
  def setTheImage(self, img):
    self.image = img
    
  def getNumberFromImage(self, config): #tesseract
    #configuration: it will read only the specified language and for what to look for
    return pytesseract.image_to_string(self.image, lang=config['TESS_LANGUAGE'], 
      config='--psm ' + config['TESS_PAGESEGMEN'] + ' --oem ' + config['TESS_OCRENGINEMODE'] 
      +' -c tessedit_char_whitelist=' + config['TESS_WHITELIST']) 
      
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
    
  outputFile = open(config['OUTPUT_FILE'],"a")
  imagesPath = Path(config['FOLDER_NAME']).glob("*.jpg")
  
  for imagePath in imagesPath:
    #pre process tesseract
    objOfImage = ImageToText(cv2.imread(str(imagePath)))
    #objOfImage.setTheImage(utils.addNoise(objOfImage.getTheImage()))
    #objOfImage.setTheImage(utils.addBrightness(objOfImage.getTheImage()))
    #cv2.imshow("e",objOfImage.image)
    #cv2.waitKey(0)
    
    startTime = time.time()
    binaryImage = objOfImage.preprocess()
    
    #cv2.imshow(str(imagePath), binaryImage)
    #cv2.waitKey(0)
    
    text = objOfImage.getNumberFromImage(config)
    text = text.replace("\n", "")
    endTime = time.time()
    ellapsedSeconds = endTime - startTime
    outputFile.write(str(imagePath) + " " + text + " " + str(round(ellapsedSeconds,3)) + "\n")
  logging.debug("Logging test...")


if __name__ == '__main__':
    main()
