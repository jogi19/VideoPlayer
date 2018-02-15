

import sys
import thread
import time
from PyQt4 import QtGui ,  QtCore,  Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from videoplayergui import Ui_Dialog as Dlg
from PyQt4.phonon import Phonon
from myvideoplayer import MyVideoWidget

try:
    from PyQt4.phonon import Phonon


except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Video Player",
            "Your Qt installation does not have Phonon support.",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class MyDialog(QtGui.QDialog, Dlg, ): 
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)
        self.verticalSliderVolume.setValue(30)
        self.desktop_widget = QDesktopWidget()
        self.numScreens = self.desktop_widget.numScreens();
        self.checkBoxScreenVisible.setChecked(1)
        self.skipnext =0
        if self.numScreens > 1:
            self.checkBoxSecondScreen.setChecked(1)
        self.lastOpenedFile = "."
        self.isSliderMoving = 0
        # add Slots
        self.connect(self.pushButtonPrevTrack,  QtCore.SIGNAL("clicked()"), self.onPushButtonPrevTrack)
        self.connect(self.pushButtonSeekPrev,  QtCore.SIGNAL("clicked()"), self.onPushButtonSeekPrev)
        self.connect(self.pushButtonPlay,  QtCore.SIGNAL("clicked()"), self.onPushButtonPlay)
        self.connect(self.pushButtonPause,  QtCore.SIGNAL("clicked()"), self.onPushButtonPause)
        self.connect(self.pushButtonStop,  QtCore.SIGNAL("clicked()"), self.onPushButtonStop)
        self.connect(self.pushButtonSeekNext,  QtCore.SIGNAL("clicked()"), self.onPushButtonSeekNext)
        self.connect(self.pushButtonNextTrack,  QtCore.SIGNAL("clicked()"), self.onPushButtonNextTrack)
        self.connect(self.verticalSliderVolume,QtCore.SIGNAL("sliderMoved(int)"), self.onSlider)
        self.connect(self.pushButtonAddFile,  QtCore.SIGNAL("clicked()"), self.onPushButtonAddFile)
        self.connect(self.pushButtonRemoveFile,  QtCore.SIGNAL("clicked()"), self.onPushButtonRemoveFile)
        self.connect(self.pushButtonMoveUp,  QtCore.SIGNAL("clicked()"), self.onPushButtonMoveUp)
        self.connect(self.pushButtonMoveDown,  QtCore.SIGNAL("clicked()"), self.onPushButtonMoveDown)
        self.connect(self.horizontalSliderVideoSize,QtCore.SIGNAL("sliderMoved(int)"), self.onHorizontalSliderVideoSize)
        self.connect(self.horizontalSliderVideoSize,QtCore.SIGNAL("sliderReleased ()"), self.onHorizontalSliderVideoSizeReleased)
        self.connect(self.checkBoxScreenVisible,QtCore.SIGNAL("clicked()"), self.onCheckBoxScreenVisible)
        self.connect(self.checkBoxPlaySingleTrack,QtCore.SIGNAL("clicked()"), self.onCheckBoxPlaySingleTrack)
        
        self.connect(self.listWidgetPlayList, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),self.onPushButtonPlay) 
        self.connect(self.horizontalSliderTrackPos, QtCore.SIGNAL("sliderMoved (int)"),self.onSliderMoved)
        self.connect(self.horizontalSliderTrackPos, QtCore.SIGNAL("sliderReleased ()"),self.onSiderReleased)
        
       
        
    #play previous track in play list   
    def onPushButtonPrevTrack(self):
        ci = self.listWidgetPlayList.currentRow()
        if (ci == 0) :
            self.listWidgetPlayList.setCurrentRow(self.listWidgetPlayList.count()-1)         # wraparound
        else:
            self.listWidgetPlayList.setCurrentRow(ci-1)
        self.startVideoplayer()
     
   # skip back 2 sec. in track    
    def onPushButtonSeekPrev(self):
        window.seekIt(-2000)
        
    # play or resume selected track
    def onPushButtonPlay(self):
        print"onPushButtonPlay"
        self.startVideoplayer()
     
    # pause running track   
    def onPushButtonPause(self):
        window.pauseIt()
    
    # stop running track and close screen window    
    def onPushButtonStop(self):
        self.labelNowPlaying.setText("no track playing")
        window.stopIt()
        window.close()
        
    # skip forward 2 sec. in track
    def onPushButtonSeekNext(self):
        window.seekIt(2000)
    
    # play next track
    def onPushButtonNextTrack(self):
        ci = self.listWidgetPlayList.currentRow()
        if (ci == (self.listWidgetPlayList.count()-1)) :
            self.listWidgetPlayList.setCurrentRow(0)         # wraparound
        else:
            self.listWidgetPlayList.setCurrentRow(ci+1)
        self.startVideoplayer()
    
    # start the video
    def startVideoplayer(self):
       screen_id = 0
       if self.numScreens>1:
           if  self.checkBoxSecondScreen.isChecked():
                screen_id = 1
       else:
           self.checkBoxSecondScreen.setChecked(0)
        
       geometry = self.desktop_widget.screenGeometry (screen_id)
       self.windowRight = geometry.right()
       self.windowLeft =  geometry.left()
       self.windowBottom = geometry.bottom()
       self.windowTop = geometry.top()
       self.height = self.windowBottom - self.windowTop+1
       self.width = self.windowRight - self.windowLeft+1
       
       if self.listWidgetPlayList.count() <= 0:
            return
       playfile = self.listWidgetPlayList.currentItem().text()
       self.m_myfileName = self.getFileName(playfile)
       window.playIt(playfile)
       
            
       window.setWindowFlags(Qt.SplashScreen)
       self.connect(window.mediaobject, QtCore.SIGNAL('tick(qint64)'),self.tick)
       window.mediaobject.setTickInterval(1000)
      
       self.connect(window.mediaobject, QtCore.SIGNAL("prefinishMarkReached (qint32)"),self.onPrefinishMarkReached)
       window.mediaobject.setPrefinishMark(1000)
       #self.connect(window.mediaobject, QtCore.SIGNAL("finished()"),self.onPrefinishMarkReached)
       self.labelNowPlaying.setText(self.m_myfileName)
       if self.checkBoxLockVideoSize.isChecked():
            print "checkBoxLockVideoSize.isChecked()"
            self.onHorizontalSliderVideoSizeReleased()
       else: 
            print "checkBoxLockVideoSize.isChecked() NO"  
            window.setGeometry(geometry)
            self.labelVideoSize_width.setText(QString.number(self.width))
            self.horizontalSliderTrackPos.setValue(self.width)
       
    # set volume
    def onSlider(self):
       slidervalue = self.verticalSliderVolume.value() 
       window.setVideoVolume(slidervalue)
    
    # add file to playlist
    def onPushButtonAddFile(self):
        self.filename = QtGui.QFileDialog.getOpenFileNames(self, "Load Video or Audio File",self.lastOpenedFile ,"*.avi;*.mp3;*.ogg" )
 
        if self.filename.isEmpty():
            return
        activateFirstEntry = 0
        if self.listWidgetPlayList.count() <=1:
             activateFirstEntry = 1
             
        self.lastOpenedFile = self.filename[0] 
        self.listWidgetPlayList.addItems(self.filename)
        # make shure, that one item is selected
        if activateFirstEntry==1:
            self.listWidgetPlayList.setCurrentRow(0) 
        
    # remove file from playlist 
    def onPushButtonRemoveFile(self):
        ci = self.listWidgetPlayList.currentRow()
        self.listWidgetPlayList.takeItem(ci)
     
    # move item up in playlist   
    def onPushButtonMoveUp(self):
        ci = self.listWidgetPlayList.currentRow()
        if (ci == 0):
            return
        listItem =self.listWidgetPlayList.takeItem(ci)
        self.listWidgetPlayList.insertItem(ci-1, listItem)
        self.listWidgetPlayList.setCurrentRow(ci-1)
    
    # move item down in playlist
    def onPushButtonMoveDown(self):
        ci = self.listWidgetPlayList.currentRow()
        if ci == self.listWidgetPlayList.count()-1:
            return
        listItem =self.listWidgetPlayList.takeItem(ci)
        self.listWidgetPlayList.insertItem(ci+1, listItem)
        self.listWidgetPlayList.setCurrentRow(ci+1)
     
    def onHorizontalSliderVideoSize(self):
       va = self.horizontalSliderVideoSize.value()
       print va
       self.labelVideoSize_width.setText(QString.number(va))
       
    def onHorizontalSliderVideoSizeReleased(self):   
       newWidth = self.horizontalSliderVideoSize.value()
       newHeight = newWidth/4*3
       newLeft = self.windowLeft+((self.width-newWidth)/2)
       newTop = self.windowTop+((self.height-newHeight)/2)
       print "newWidth"
       print newWidth
       window.setGeometry(newLeft, newTop, newWidth, newHeight)
       
       
    def onCheckBoxPlaySingleTrack(self):
        if self.checkBoxPlaySingleTrack.isChecked():
            self.isPlaynextTrack=1
        else:
            self.isPlaynextTrack=0    
    
    
    def onCheckBoxScreenVisible(self):
        
        if self.checkBoxScreenVisible.isChecked():
            window.showFullScreen()
        else:
            window.close()
          
    def onSliderMoved(self):
        self.isSliderMoving = 1
        print "onSliderMoved(self)"
        self.sliderPos = self.horizontalSliderTrackPos.sliderPosition()
        print self.sliderPos
        sliderTime = displayTime = QtCore.QTime(0, (self.sliderPos / 60000) % 60, (self.sliderPos / 1000) % 60)
        self.lcdNumberTrackTime.display(sliderTime.toString('mm:ss'))
        sliderTimeRemain = self.horizontalSliderTrackPos.maximum()-self.sliderPos
        displayTimeSliderTimeRemain  = QtCore.QTime(0, (sliderTimeRemain / 60000) % 60, (sliderTimeRemain / 1000) % 60)    
        self.lcdNumberRemainingTime.display(displayTimeSliderTimeRemain.toString('mm:ss'))
        
    def onSiderReleased(self):
        window.mediaobject.seek(self.sliderPos)
        self.isSliderMoving = 0
        
    def onPrefinishMarkReached(self):
        print "onPrefinishMarkReached"
        if self.checkBoxPlaySingleTrack.isChecked():
            self.labelNowPlaying.setText("no track playing")
            return
        ci = self.listWidgetPlayList.currentRow()
        pc = self.listWidgetPlayList.count()
        if ci == (pc-1):
            window.close()
            return
        else:
            self.onPushButtonNextTrack()
        
    
    def getFileName(self, pathname):
        p_pathname = QString(pathname)
        posSlash= p_pathname.lastIndexOf("/", -1)
        fn = p_pathname.remove (0, posSlash+1)
        return fn
        
    def tick(self, ptime):
        if self.isSliderMoving == 0:   #avoid update while slider is moving
            displayTime = QtCore.QTime(0, (ptime / 60000) % 60, (ptime / 1000) % 60)
            self.lcdNumberTrackTime.display(displayTime.toString('mm:ss'))
            totaltime =  window.mediaobject.totalTime()
            displayTotaltime = QtCore.QTime(0, (totaltime / 60000) % 60, (totaltime / 1000) % 60) 
            self.labelNowPlaying.setText(self.m_myfileName+" / "+displayTotaltime.toString('mm:ss'))
            remainingTime = totaltime - ptime
            displayTime = QtCore.QTime(0, (remainingTime / 60000) % 60, (remainingTime / 1000) % 60)    
            self.lcdNumberRemainingTime.display(displayTime.toString('mm:ss'))
            self.horizontalSliderTrackPos.setMaximum(totaltime)
            self.horizontalSliderTrackPos.setSliderPosition(ptime)
    
app = QtGui.QApplication(sys.argv) 
window = MyVideoWidget()
dialog = MyDialog() 
dialog.show() 
sys.exit(app.exec_())
