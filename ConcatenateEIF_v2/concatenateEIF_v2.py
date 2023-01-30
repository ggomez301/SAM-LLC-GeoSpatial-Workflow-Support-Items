##########################################
##  Written by: Guillermo Gomez
##  Geospatial Technical Support
##  SAM LLC
##  This python GUI script looks at EIF files and concatenates all files into one EIF file that can
##   be opened as a TXT file. Can be used for multiple file locations or if wanted put general path
##   in and script can look in various existing files to read EIF files.
##   Instructions:
##   1. Copy directory of path needed to concatenate EIF files.
##   2. Paste the directory and hit submit.
##   3. Click restart if needed.
##########################################

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import os
import datetime
import sys
import csv

class MyWindow(QMainWindow):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    #Window size variables
    xpos = 200
    ypos = 200
    width = 500
    height = 500

    #Initialization method
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(self.xpos, self.ypos, self.width, self.height)
        self.setWindowTitle("ConcatenateEIF")
        self.initUI()
        
    #GUI initialization method
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)

        self.label2.move(100, 60)
        self.pixmap = QPixmap('SAM_Image.png')
        self.label2.setPixmap(self.pixmap)
        self.label2.resize(self.pixmap.width(),
                          self.pixmap.height())

        #User input to enter directory
        self.label.setText("Enter 04_CAM_RAW\\01_EIF\\PhaseOne_IX100 directory:")
        self.label.move(100, 250)
        self.update()

        self.userLine = QtWidgets.QLineEdit(self)
        self.userLine.move(100, 280)
        self.userLine.resize (300, 25)

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Submit")
        self.button1.move(200, 320)
        self.button1.clicked.connect(self.clicked)

    #Method when user enters directory and clicks submit
    def clicked(self):
        self.label.hide()

        #Concatenate method call
        self.concatenate()

        self.label1.move(50, 200)
        self.label1.setText("EIF's concated in 'Total' file and stored in current directory: \n\n" + self.current_dir)
        self.update()

        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("Restart")
        self.button2.move(200, 360)
        self.userLine.hide()
        self.button1.hide()
        self.button2.show()
        self.button2.clicked.connect(self.restartClicked)

    #Method to Concatenate EIF's and write into 'Total' .eif file
    def concatenate(self):
        user_dir = self.userLine.text()
        self.current_dir = user_dir

        self.label.hide()

        PATHS = [
            user_dir
        ]
        outfile = 'total ' + str(datetime.datetime.now()).replace(':','_').replace('-','_') + '.eif'

        header = '#time[s];file;sequenceID;roll[deg];pitch[deg];yaw[deg];omega[deg];phi[deg];kappa[deg];latitude[deg];longitude[deg];altitude[m];rollRate[deg/s];pitchRate[deg/s];yawRate[deg/s];exposure[s];gain[dB];iso;aperture;gsd[m];blur[px]\n'
        output=[]
        output.append(header)
        for path in PATHS:
            for fl in os.listdir(path):
                if os.path.isfile(os.path.join(path, fl)) and fl[-4:] == '.eif':
                    with open(os.path.join(path, fl), 'r')as f:
                        content = f.readlines()
                        output.extend(content[4:])


        with open(os.path.join(self.current_dir, outfile), 'w') as f:
            f.writelines(output)

    #Method to restart application
    def restartClicked(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Method to adjust label sizes
    def update(self):
        self.label.adjustSize()
        self.label1.adjustSize()

#'main' method to open window
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    
#window() method call
window()
