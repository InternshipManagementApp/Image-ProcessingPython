#!/usr/bin/env python

import cv2, numpy 
import pytesseract
from configparser import ConfigParser
import logging.config
from pathlib import Path 
import utils

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Anita\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' 

class ImageToText:
  def __init__ (self, image):
    self.image = image
    
  def preprocess(self):
    grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.medianBlur(grayImage,5)
    _, binaryImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_OTSU)
    binaryImage = utils.invertBlackAndWhite(binaryImage)
    erodeImg = utils.erode(binaryImage)
    dilateImg = utils.dilate(erodeImg)
    openingImg = utils.opening(dilateImg)
    return openingImg

  def getTheImage(self):
    return self.image
    
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
    binaryImage = objOfImage.preprocess()
    
    cv2.imshow(str(imagePath), binaryImage)
    cv2.waitKey(0)
    
    text = objOfImage.getNumberFromImage(config)
    outputFile.write(str(imagePath) + " " +text)
  logging.debug("Logging test...")  


if __name__ == '__main__':
    main()
