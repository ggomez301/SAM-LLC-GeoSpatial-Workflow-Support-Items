##########################################
##  Written by: Guillermo Gomez
##  Geospatial Technical Support
##  SAM LLC
##  This python GUI program provides a QC Check on all incoming data
##   Instructions:
##   1. Connect drive into machine
##   2. Copy directory path of job.
##   3. Run the program and paste job directory and click Submit.
##########################################

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import os
import csv

#Window size variables
xpos = 200
ypos = 200
width = 500
height = 500

class MyWindow(QMainWindow):    

    #Variables used to check count of specific files for QC Check
    rxps = 0
    c1rxps = 0
    c2rxps = 0  
    zifs = 0
    c1zifs = 0
    c2zifs = 0
    iiqs = 0
    tifs = 0

    xpos = 200
    ypos = 200
    width = 700
    height = 700

    dirname = "*"
    c1dirname = "*"
    c2dirname = "*"
    
    #Channel 1 and Channel 2 directory initialization for later use
    channel1Path = "\\03_RIEGL_RAW\\02_RXP\\Channel_1" 
    channel2Path = "\\03_RIEGL_RAW\\02_RXP\\Channel_2"

    #String variables to compare file names
    rName = '.rxp'
    zName = '.zif'
    iName = '.iiq'
    tName = '.tif'

    #Initialization method
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle("SAM LLC Incoming Data QC Check")
        self.initUI()
    #GUI initialization method    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)
        self.label4 = QtWidgets.QLabel(self)
        self.label5 = QtWidgets.QLabel(self)
        self.label6 = QtWidgets.QLabel(self)
        self.label7 = QtWidgets.QLabel(self)
        self.label8 = QtWidgets.QLabel(self)
        self.label9 = QtWidgets.QLabel(self)
        self.label10 = QtWidgets.QLabel(self)

        self.label10.move(200, 60)
        self.pixmap = QPixmap('SAM_Image.png')
        self.label10.setPixmap(self.pixmap)
        self.label10.resize(self.pixmap.width(),
                          self.pixmap.height())

        #User input to find job directory 
        self.label1.setText("Enter Data directory")
        self.label1.move(300, 200)

        self.userLine = QtWidgets.QLineEdit(self)
        self.userLine.move(200, 280)
        self.userLine.resize (300, 25)
        
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Submit")
        self.button1.move(300, 320)
        self.button1.clicked.connect(self.clicked)

    #Method when user enters directory and clicks submit
    def clicked(self):
        print ("\nentering clicked method")
        
        self.dirname = self.userLine.text()
        self.dirname.strip()
        self.c1dirname = self.dirname + self.channel1Path
        self.c2dirname = self.dirname + self.channel2Path

        #Method calls
        
        self.rxps = self.filecheck(self.rName)
        self.c1rxps = self.c1filecheck(self.rName)
        self.c2rxps = self.c2filecheck(self.rName)
        self.zifs = self.filecheck(self.zName)
        self.c1zifs = self.c1filecheck(self.zName)
        self.c2zifs = self.c2filecheck(self.zName)
        self.iiqs = self.filecheck(self.iName)
        self.tifs = self.filecheck(self.tName)

        print("\nMethods called")

        self.label10.hide()

        self.label.move(50, 60)
        self.label.setText("Checking in directory: " + self.dirname)
        self.update()
        
        self.label1.move(50, 80)
        self.label1.setText("Number of RXP files in \\03_RIEGL_RAW\\02_RXP\\Channel_1: %i" % self.c1rxps)
        self.update()

        self.label2.move(50, 100)
        self.label2.setText("Number of RXP files in \\03_RIEGL_RAW\\02_RXP\\Channel_2: %i" % self.c2rxps)
        self.update()
        
        print("\nprinted labels")
        
        self.label3.move(50, 120)
        self.label3.setText("Total number of RXP files: %i" % self.rxps)
        self.update()

        self.label4.move(50,140)
        self.label4.setText("Number of ZIF files in \\03_RIEGL_RAW\\02_RXP\\Channel_1: %i" % self.c1zifs)
        self.update()

        self.label5.move(50,160)
        self.label5.setText("Number of ZIF files in \\03_RIEGL_RAW\\02_RXP\\Channel_2: %i" % self.c2zifs)
        self.update()

        self.label6.move(50,180)
        self.label6.setText("Total number of ZIF files: %i" % self.zifs)
        self.update()

        self.label7.move(50,200)
        self.label7.setText("Number of IIQ files in \\04_CAM_RAW\\03_IMG\\Camera_RGB: %i" % self.iiqs)
        self.update()

        self.label8.move(50,220)
        self.label8.setText("Number of TIF files in \\04_CAM_RAW\\04_MON\\Camera_RGB: %i" % self.tifs)
        self.update()

        self.label9.move(50,240)
        self.label9.setText("CSV File with results created in project directory!")
        self.update()

        print("\nWriting CSV")

        self.csvWriter()

        print("\nWriting done")

        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("Restart")
        self.button2.move(300, 360)
        self.userLine.hide()
        self.button1.hide()
        self.button2.show()
        self.button2.clicked.connect(self.restartClicked)

    #Method to restart application
    def restartClicked(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Method to adjust label sizes
    def update(self):
        self.label.adjustSize()
        self.label1.adjustSize()
        self.label2.adjustSize()
        self.label3.adjustSize()
        self.label4.adjustSize()
        self.label5.adjustSize()
        self.label6.adjustSize()
        self.label7.adjustSize()
        self.label8.adjustSize()
        self.label9.adjustSize()

    #Method to check total number of .rxp, .zif, iiq, and .tif files
    def filecheck(self, fileType):
        fileCounter = 0
        for root, dirs, files in os.walk(self.dirname):
            for file in files:
                if file.endswith(fileType):
                    fileCounter += 1
            
        return fileCounter

    #Method to check total number of .rxp and .zif files for Channel 1
    def c1filecheck(self, fileType):
        fileCounter = 0
        for root, dirs, files in os.walk(self.c1dirname):
            for file in files:
                if file.endswith(fileType):
                    fileCounter += 1
            
        return fileCounter

    #Method to check total number of .rxp and .zif files for Channel 2
    def c2filecheck(self, fileType):
        fileCounter = 0
        for root, dirs, files in os.walk(self.c2dirname):
            for file in files:
                if file.endswith(fileType):
                    fileCounter += 1
            
        return fileCounter

    #Method to write results into .CSV file within project directory
    def csvWriter(self):
        header = ["Total RXPs","Ch1 RXPs", "Ch2 RXPs", "Ch1 ZIFs", "Ch2 ZIFs", "Total ZIFs", "IIQs", "TIFs"]
        data = [self.rxps, self.c1rxps, self.c2rxps, self.c1zifs, self.c2zifs, self.zifs, self.iiqs, self.tifs]

        
        with open(os.path.join(self.dirname, "QC_Check_Results" +'.csv'), 'w', newline= '') as csvfile:
            writer = csv.writer(csvfile)
        
            writer.writerow(header)
            writer.writerow(data)
        
#'main' method to open window
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    
#window() method call
window()
