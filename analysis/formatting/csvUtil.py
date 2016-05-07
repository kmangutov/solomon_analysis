import csv

class CSVFile:

  def __init__(self, fileName, subdir='render/'):
    self.fileName = fileName
    self.file = open(subdir + fileName, 'wb+') 

  def write(self, text):
    self.file.write(text + "\n")

  def writeA(self, array):
    self.write(",".join(array))

  def close(self):
    self.file.close()




