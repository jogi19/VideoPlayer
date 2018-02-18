#!/usr/bin/env python
 
# simple testapplication that runs videos using 
# the Phonon framework is brought to you by
# jogi19 for the changingsong project
# http://sourceforge.net/projects/changingsong/
from __future__ import print_function 
import sys
import time


from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import PyQt5.QtMultimedia as Phonon


try:
    import PyQt5.QtMultimedia as Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Video Player",
            "Your Qt installation does not have Phonon support.",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.NoButton)
    sys.exit(1)
 
class MyVideoWidget(Phonon.VideoWidget):

     def __init__(self):
        QtGui.QMainWindow.__init__(self) 
        
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.volume = 0.3 #default value
        self.isPaused = 0
        self.pausedTime = 0
        
     #stop currend file
     def stopIt(self):
         self.mediaobject.stop()
         
     #play selected file or resume after pause    
     def playIt(self, playfile):
        self.audioOutput = Phonon.AudioOutput(Phonon.VideoCategory, self)
        self.currentFile= playfile
        self.mediasource = Phonon.MediaSource(self.currentFile)
        self.mediaobject = Phonon.MediaObject()
        self.mediaobject.setCurrentSource(self.mediasource)
        Phonon.createPath(self.mediaobject, self)# test
        self.connect(self.mediaobject,QtCore.SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.stateChanged)
        Phonon.createPath(self.mediaobject, self.audioOutput) 
        self.audioOutput.setVolume(self.volume)   
        self.mediaobject.pause() #check if this prevents hang on next track
        self.mediaobject.play()
        
       
     # pause current running file   
     def pauseIt(self):
        self.mediaobject.pause()
     
     # seek in current file. 
     def seekIt(self, milisec):
        currentTime = self.mediaobject.currentTime()
        jumpToTime = currentTime+milisec
        self.mediaobject.seek(jumpToTime)
     
        
     # set valume in percent in a range of 0% -100% 
     def setVideoVolume(self, volumePercent):
        volumeValue = volumePercent/100.0
        self.volume = volumeValue 
        self.audioOutput.setVolume(self.volume)
        
     def stateChanged(self, newState, oldState):
         if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                print("newState == Phonon.ErrorState:")
            else:
                print("error")
 
         elif newState == Phonon.PlayingState:
            print("newState == Phonon.PlayingState:")
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
            
         elif newState == Phonon.StoppedState:
            print("newState == Phonon.StoppedState:")
 
         elif newState == Phonon.PausedState:
            print("newState == Phonon.PausedState:")
            self.pausedTime = self.mediaobject.currentTime()
            self.isPaused = 1
            
         elif newState == Phonon.LoadingState:
            print("newState == Phonon.LoadingState")
                
     

