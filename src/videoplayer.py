

import sys
from PyQt5 import QtGui, QtCore, Qt, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import *
from videoplayergui import Ui_Dialog as Dlg
from myvideoplayer import MyVideoWidget

class MyDialog(QtWidgets.QDialog,Dlg):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.verticalSliderVolume.setValue(30)
        self.desktop_widget = QtWidgets.QDesktopWidget()
        app = QtGui.QGuiApplication
        #QtWidgets.QtGui
        all_screens = app.screens()
        #self.numScreens = self.desktop_widget.numScreens() #TODO needs to figure out, why this is not working
        self.numScreens = len(all_screens)
        print("self.numScreens: "+str(self.numScreens))
        self.checkBoxScreenVisible.setChecked(1)
        self.skipnext = 0
        if self.numScreens > 1:
            self.checkBoxSecondScreen.setChecked(1)
        self.lastOpenedFile = "."
        self.isSliderMoving = 0
        print('### 1 ###')
        # add Slots
        # TODO switch to new style signal/slot http://pyqt.sourceforge.net/Docs/PyQt4/new_style_signals_slots.html
        # https://pythonspot.com/pyqt5-signals-and-slots/
        self.pushButtonPrevTrack.clicked.connect(self.onPushButtonPrevTrack)
        self.pushButtonSeekPrev.clicked.connect(self.onPushButtonSeekPrev)
        self.pushButtonPlay.clicked.connect(self.onPushButtonPlay)
        self.pushButtonPause.clicked.connect(self.onPushButtonPause)
        self.pushButtonStop.clicked.connect(self.onPushButtonStop)
        self.pushButtonSeekNext.clicked.connect(self.onPushButtonSeekNext)
        self.pushButtonNextTrack.clicked.connect(self.onPushButtonNextTrack)
        self.verticalSliderVolume.sliderMoved.connect(self.onSlider)
        self.pushButtonAddFile.clicked.connect(self.onPushButtonAddFile)
        self.pushButtonRemoveFile.clicked.connect(self.onPushButtonRemoveFile)
        self.pushButtonMoveUp.clicked.connect(self.onPushButtonMoveUp)
        self.pushButtonMoveDown.clicked.connect(self.onPushButtonMoveDown)
        self.horizontalSliderVideoSize.sliderMoved.connect(self.onHorizontalSliderVideoSize)
        self.horizontalSliderVideoSize.sliderReleased.connect(self.onHorizontalSliderVideoSizeReleased)
        self.checkBoxScreenVisible.clicked.connect(self.onCheckBoxScreenVisible)
        self.checkBoxPlaySingleTrack.clicked.connect(self.onCheckBoxPlaySingleTrack)
        self.listWidgetPlayList.itemDoubleClicked.connect(self.onPushButtonPlay)
        self.horizontalSliderTrackPos.sliderMoved.connect(self.onSliderMoved)
        self.horizontalSliderTrackPos.sliderReleased.connect(self.onSiderReleased)

        self.windowRight = 0
        self.windowLeft = 0
        self.windowBottom = 0
        self.windowTop = 0
        self.height = 0
        self.width = 0
        
    #play previous track in play list
    def onPushButtonPrevTrack(self):
        ci = self.listWidgetPlayList.currentRow()
        if (ci == 0):
            self.listWidgetPlayList.setCurrentRow(self.listWidgetPlayList.count()-1) # wraparound
        else:
            self.listWidgetPlayList.setCurrentRow(ci-1)
        self.startVideoplayer()

   # skip back 2 sec. in track    
    def onPushButtonSeekPrev(self):
        WINDOW.seekIt(-2000)

    # play or resume selected track
    def onPushButtonPlay(self):
        print("onPushButtonPlay")
        self.startVideoplayer()

    # pause running track
    def onPushButtonPause(self):
        WINDOW.pauseIt()

    # stop running track and close screen WINDOW
    def onPushButtonStop(self):
        self.labelNowPlaying.setText("no track playing")
        WINDOW.stopIt()
        WINDOW.close()

    # skip forward 2 sec. in track
    def onPushButtonSeekNext(self):
        WINDOW.seekIt(2000)

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
       WINDOW.playIt(playfile)

       WINDOW.setWindowFlags(Qt.SplashScreen)
       #self.connect(WINDOW.mediaobject, QtCore.SIGNAL('tick(qint64)'),self.tick)
       #WINDOW.mediaobject.tick.connect(self.tick) # TODO figure out how tp get the ticks
       #WINDOW.mediaobject.setTickInterval(1000)
       
       #self.connect(WINDOW.mediaobject, QtCore.SIGNAL("prefinishMarkReached (qint32)"),self.onPrefinishMarkReached)
       #WINDOW.mediaobject.finished.connect(self.onPrefinishMarkReached)
       #WINDOW.mediaobject.setPrefinishMark(1000)
       #self.connect(WINDOW.mediaobject, QtCore.SIGNAL("finished()"),self.onPrefinishMarkReached)
       self.labelNowPlaying.setText(self.m_myfileName)
       if self.checkBoxLockVideoSize.isChecked():
            print("checkBoxLockVideoSize.isChecked()")
            self.onHorizontalSliderVideoSizeReleased()
       else: 
            print("checkBoxLockVideoSize.isChecked() NO")  
            WINDOW.setGeometry(geometry)
            self.labelVideoSize_width.setText(str(self.width))
            self.horizontalSliderTrackPos.setValue(self.width)

    # set volume
    def onSlider(self):
       slidervalue = self.verticalSliderVolume.value() 
       WINDOW.setVideoVolume(slidervalue)

    # add file to playlist
    def onPushButtonAddFile(self):
        print('self.lastOpendFile1: '+str(self.lastOpenedFile))
        self.filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Load Video or Audio File",self.lastOpenedFile ,"*.*" )
        print("self.filename: "+str(self.filename))
        if len(self.filename) <= 0:
            return
        activateFirstEntry = 0
        if self.listWidgetPlayList.count() <=1:
             activateFirstEntry = 1

        self.lastOpenedFile = str(self.filename[0])
        print('self.lastOpendFile2: '+self.lastOpenedFile)
        self.listWidgetPlayList.addItems(self.filename[0])
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
        print(va)
        self.labelVideoSize_width.setText(str(va))

    def onHorizontalSliderVideoSizeReleased(self):   
        newWidth = self.horizontalSliderVideoSize.value()
        newHeight = newWidth/4*3
        newLeft = self.windowLeft+((self.width-newWidth)/2)
        newTop = self.windowTop+((self.height-newHeight)/2)
        print("newWidth")
        print(newWidth)
        WINDOW.setGeometry(newLeft, newTop, newWidth, newHeight)

    def onCheckBoxPlaySingleTrack(self):
        if self.checkBoxPlaySingleTrack.isChecked():
            self.isPlaynextTrack=1
        else:
            self.isPlaynextTrack=0    

    def onCheckBoxScreenVisible(self):
        
        if self.checkBoxScreenVisible.isChecked():
            WINDOW.showFullScreen()
        else:
            WINDOW.close()

    def onSliderMoved(self):
        self.isSliderMoving = 1
        print("onSliderMoved(self)")
        self.sliderPos = self.horizontalSliderTrackPos.sliderPosition()
        print(self.sliderPos)
        sliderTime = displayTime = QtCore.QTime(0, (self.sliderPos / 60000) % 60, (self.sliderPos / 1000) % 60)
        self.lcdNumberTrackTime.display(sliderTime.toString('mm:ss'))
        sliderTimeRemain = self.horizontalSliderTrackPos.maximum()-self.sliderPos
        displayTimeSliderTimeRemain  = QtCore.QTime(0, (sliderTimeRemain / 60000) % 60, (sliderTimeRemain / 1000) % 60)    
        self.lcdNumberRemainingTime.display(displayTimeSliderTimeRemain.toString('mm:ss'))

    def onSiderReleased(self):
        WINDOW.mediaobject.seek(self.sliderPos)
        self.isSliderMoving = 0

    def onPrefinishMarkReached(self):
        print("onPrefinishMarkReached")
        if self.checkBoxPlaySingleTrack.isChecked():
            self.labelNowPlaying.setText("no track playing")
            return
        ci = self.listWidgetPlayList.currentRow()
        pc = self.listWidgetPlayList.count()
        if ci == (pc-1):
            WINDOW.close()
            return
        else:
            self.onPushButtonNextTrack()


    def getFileName(self, pathname):
        p_pathname = str(pathname)
        print('p_pathname: '+p_pathname)
        #posSlash= p_pathname.rindex("/", -1)
        posSlash= p_pathname.rindex("/")
        #fn = p_pathname.remove(0, posSlash+1)
        fn = p_pathname[posSlash+1:]
        print('fn: '+fn)
        return fn

    def tick(self, ptime):
        if self.isSliderMoving == 0:   #avoid update while slider is moving
            displayTime = QtCore.QTime(0, (ptime / 60000) % 60, (ptime / 1000) % 60)
            self.lcdNumberTrackTime.display(displayTime.toString('mm:ss'))
            totaltime =  WINDOW.mediaobject.totalTime()
            displayTotaltime = QtCore.QTime(0, (totaltime / 60000) % 60, (totaltime / 1000) % 60) 
            self.labelNowPlaying.setText(self.m_myfileName+" / "+displayTotaltime.toString('mm:ss'))
            remainingTime = totaltime - ptime
            displayTime = QtCore.QTime(0, (remainingTime / 60000) % 60, (remainingTime / 1000) % 60)    
            self.lcdNumberRemainingTime.display(displayTime.toString('mm:ss'))
            self.horizontalSliderTrackPos.setMaximum(totaltime)
            self.horizontalSliderTrackPos.setSliderPosition(ptime)
    
APP = QtWidgets.QApplication(sys.argv) 
WINDOW = MyVideoWidget()
DIALOG = MyDialog() 
DIALOG.show() 
sys.exit(APP.exec_())
