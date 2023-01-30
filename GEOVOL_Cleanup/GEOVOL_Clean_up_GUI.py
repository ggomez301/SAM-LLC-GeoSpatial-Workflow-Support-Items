##########################################
##  Written by: Guillermo Gomez
##  Geospatial Technical Support
##  SAM LLC
##
##  This python GUI script has three options to clean up the desired GEOVOL:
##   1. Deletes 02_RAW_DATA from its directories
##   2. Deletes .las files from 05_LIDAR directories
##   3. Deletes .tif files from 06_ORTHO directories
##
##   Instructions:
##   1. Copy the GEOVOL directory
##   2. Paste the directory and hit submit.
##   3. Select Clean up option
##   3. Click restart if needed.
##########################################

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import os, shutil
import csv
import errno, stat
import sys

class MyWindow(QMainWindow):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    deleted_list = []
    excludes = ['AER', 'UAS', 'SUE', 'ASBT', 'BNDY', 'CTRL', 'PIPE', 'STAK', 'TOPO', 'OTHR', 'MOB', 'SurveyControl', 'YYYYMMDD']
    root_path = ""

    #Window size variables
    xpos = 200
    ypos = 200
    width = 500
    height = 500

    #Initialization method
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle("02_Raw_Data_Clean_up")
        self.initUI()

    #GUI initialization method
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.samLabel = QtWidgets.QLabel(self)

        self.samLabel.move(100, 60)
        self.pixmap = QPixmap('SAM_Image.png')
        self.samLabel.setPixmap(self.pixmap)
        self.samLabel.resize(self.pixmap.width(),
                          self.pixmap.height())

        #User input to enter GEOVOL directory
        self.label.setText("Enter GEOVOL directory:")
        self.label.move(200, 250)
        self.update()

        self.userLine = QtWidgets.QLineEdit(self)
        self.userLine.move(100, 280)
        self.userLine.resize (300, 25)

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Submit")
        self.button1.move(200, 320)
        self.button1.clicked.connect(self.clicked)
        self.button6 = QtWidgets.QPushButton(self)
        self.button6.setText("Back")
        self.button6.move(200, 360)
        self.button6.clicked.connect(self.clicked)
        self.button6.hide()
        
    #Method when user enters directory and clicks submit
    def clicked(self):
        self.label.hide()
        self.samLabel.hide()

        self.root_path = self.userLine.text()

        self.label1.move(50, 30)
        self.label1.setText("Current GEOVOL: " + self.root_path)
        self.update()

        self.label2.move(160, 80)
        self.label2.setText("Please select type of GEOVOL cleanup: ")
        self.update()

        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("02_Raw_Data: Cleanup")
        self.button2.setGeometry(170, 120, 160, 40)

        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setText("05_LIDAR: Remove .las")
        self.button3.setGeometry(170, 180, 160, 40)

        self.button4 = QtWidgets.QPushButton(self)
        self.button4.setText("06_ORTHO: Remove .tif")
        self.button4.setGeometry(170, 240, 160, 40)

        self.button5 = QtWidgets.QPushButton(self)
        self.button5.setText("Restart")
        self.button5.move(200, 360)
        self.userLine.hide()
        self.button1.hide()
        self.button2.show()
        self.button3.show()
        self.button4.show()
        self.button5.show()

        self.button2.clicked.connect(self.cleanupRawDataClicked)
        self.button3.clicked.connect(self.removeLasClicked)
        self.button4.clicked.connect(self.removeTifClicked)
        self.button5.clicked.connect(self.restartClicked)

    #Method when user chooses Clean RAW Data option
    def cleanupRawDataClicked(self):  
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.hide()
        self.label.show()
        self.button6.show()  

        self.label.move(100, 80)
        self.label.setText("Cleaning directories 02_Raw_Data for GEOVOL: \n\n" + self.root_path)
        self.update()

        self.cleanupRawData()

        self.label1.move(100, 200)
        self.label1.setText("...done.")
        self.update()

        self.label2.move(100, 240)
        self.label2.setText("CSV file 'deletedlist' created")
        self.update() 

    #Method when user chooses 'Remove .LAS' option   
    def removeLasClicked(self):
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.hide()
        self.button6.show()

        self.label1.move(100, 80)
        self.label1.setText("Removing .las files in 05_LIDAR directories for GEOVOL: \n\n" + self.root_path)
        self.update()

        self.removeLasFiles()

        self.label2.move(100, 200)
        self.label2.setText("...done.")
        self.update()
    
    #Method when user chooses 'Remove .TIF' option
    def removeTifClicked(self):
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.hide()
        self.button6.show()

        self.label1.move(100, 80)
        self.label1.setText("Removing .tif files in 06_ORTHO directories for GEOVOL: \n\n" + self.root_path)
        self.update()

        self.removeTifFiles()

        self.label2.move(100, 200)
        self.label2.setText("...done.")
        self.update()
    
    #Method to clean up RAW Data in GEOVOL
    def cleanupRawData(self):
        self.current_dir = self.root_path

        for _root, _dirs, _files in os.walk(self.root_path, topdown=False):
            for _d in _dirs:
                if _d == "02_Raw_Data":
                    for root, dirs, files in os.walk(os.path.join(_root, _d), topdown=True):
                        dirs[:] = [d for d in dirs if d not in self.excludes]
                        dirs[:] = [d for d in dirs if not d[0] == '.']        
                        files = [f for f in files if not f[0] == '.']
                        for f in files:
                            filepath = os.path.join(root, f)
                            try:
                                os.unlink(filepath)
                                self.deleted_list.append(filepath)
                            except Exception:
                                pass
                        for d in dirs:
                            for r, directories, files in os.walk(os.path.join(root, d)):
                                for folder in directories:
                                    self.deleted_list.append(os.path.join(r, folder))
                                for file in files:
                                    self.deleted_list.append(os.path.join(r, file))
                            try:        
                                shutil.rmtree(os.path.join(root, d))
                            except Exception:
                                pass
        self.createList()
    
    #Method to remove .las files in GEOVOL
    def removeLasFiles(self):
        for _root, _dirs, _files in os.walk(self.root_path, topdown=False):
            for _d in _dirs:
                if _d == "05_LiDAR":
                    for root, dirs, files in os.walk(os.path.join(_root, _d), topdown=False):
                        for f in files:
                            base, ext = os.path.splitext(os.path.join(root, f))
                            if ext == '.las':
                               os.unlink(os.path.join(root, f))
    
    #Method to remove .tif files in GEOVO
    def removeTifFiles(self):
        for _root, _dirs, _files in os.walk(self.root_path, topdown=False):
            for _d in _dirs:
                if _d == "06_Ortho":
                    for root, dirs, files in os.walk(os.path.join(_root, _d), topdown=False):
                        for f in files:
                            base, ext = os.path.splitext(os.path.join(root, f))
                            if ext == '.tif':
                               os.unlink(os.path.join(root, f))

    #Method to create csv file of deleted data
    def createList(self):
        with open('deletedlist.csv', mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filepath'])                        
            for item in self.deleted_list:
                writer.writerow([item])

    #Don't know if I really need this method? I'm going to keep it in here just in case...            
    def readonly_handler(self, func, path, execinfo): 
        os.chmod(path, 128) 
        func(path)

    #Method to restart application
    def restartClicked(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Method to adjust label sizes
    def update(self):
        self.label.adjustSize()
        self.label1.adjustSize()
        self.label2.adjustSize()

#'main' method to open window
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    
#window() method call
window()
