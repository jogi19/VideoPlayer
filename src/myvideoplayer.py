#!/usr/bin/env python
 
# simple testapplication that runs videos using 
# the Phonon framework is brought to you by
# jogi19 for the changingsong project
# http://sourceforge.net/projects/changingsong/
from __future__ import print_function 
import sys
import time


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimediaWidgets import *

try:
    import PyQt5.QtMultimedia as MM
    
except ImportError:
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "Video Player",
            "Your Qt installation does not have Phonon support.",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Default,
            QtWidgets.QMessageBox.NoButton)
    sys.exit(1)
 
class MyVideoWidget(QVideoWidget):

     def __init__(self):
        QtWidgets.QMainWindow.__init__(self) 
        
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.volume = 0.3 #default value
        self.isPaused = 0
        self.pausedTime = 0
        self.format = MM.QAudioFormat()
        self.player = MM.QMediaPlayer()
        self.isStopped = False;  
        
     #stop currend file
     def stopIt(self):
         self.isStopped = True
         self.player.stop()
         
         
     #play selected file or resume after pause    
     def playIt(self, playfile):
         
      # Set up the format, eg.
      # OLD
        self.isStopped = True
        w = QVideoWidget()
        w.show()
        print("playfile: "+playfile)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(playfile)))
        self.player.setVideoOutput(w)
        self.player.play()
        sys.exit(app.exec_())
       
     # pause current running file   
     def pauseIt(self):
        self.player.pause()
     
     # seek in current file. 
     def seekIt(self, milisec):
        currentTime = self.mediaobject.currentTime()
        jumpToTime = currentTime+milisec
        self.mediaobject.seek(jumpToTime)
     
        
     # set valume in percent in a range of 0% -100% 
     def setVideoVolume(self, volumePercent):
        volumeValue = volumePercent/100.0
        self.player.setVolume(volumeValue)
        
        
     def stateChanged(self, newState, oldState):
         if newState == MM.ErrorState:
            if self.mediaObject.errorType() == MM.FatalError:
                print("newState == MM.ErrorState:")
            else:
                print("error")
 
         elif newState == MM.PlayingState:
            print("newState == MM.PlayingState:")
            print("has video")
            print(self.mediaobject.hasVideo())
            if not self.mediaobject.hasVideo():
                self.close()
            else:
                self.show()
            if self.isPaused ==1:
                self.mediaobject.seek(self.pausedTime)
            self.pausedTime = 0         
            self.isPaused = 0        
            
         elif newState == MM.StoppedState:
            print("newState == MM.StoppedState:")
 
         elif newState == MM.PausedState:
            print("newState == MM.PausedState:")
            self.pausedTime = self.mediaobject.currentTime()
            self.isPaused = 1
            
         elif newState == MM.LoadingState:
            print("newState == MM.LoadingState")