# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:43:49 2016

@author: matsumoto
"""
import os
import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import matplotlib as plt
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy.random import randn

### Analyze
def Analyze(filename):
    global fileProgressBar 
    global ListWin
    
    i=0
    with open(filename) as f:
        fileProgressBar.setRange(0, len(f.readline()))
        
        for line in f:
            i = i+1
            fileProgressBar.setValue(i)
            
            list = line.strip('\n')
            list = list.split(',')
            
            for n in range(0, (len(list)-2)/6):
                waku=pd.DataFrame({'filename':[list[0]],
                              'frame':[list[1]],
                              'magid':[list[2+6*n]],
                              'scanid':[list[3+6*n]],
                              'widthX':[list[4+6*n]],
                              'widthY':[list[5+6*n]],
                              'centerX':[list[6+6*n]],
                              'centerY':[list[7+6*n]]})
                              
                ListWin.setItem(waku)   
                wakulist=pd.concat([wakulist, waku])
               
    return True

### MainWindow
class MainWindow(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.loadSetting()
    
    def loadSetting(self):
        print 'loadSetting'
        self.settings = QtCore.QSettings('setting.ini', QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('MainWindow')
            geometry=self.settings.value('geometry')
            if (geometry != None):
                self.restoreGeometry(geometry)
            self.settings.endGroup()
    
    def initUI(self):
        print 'initUI'
        self.setGeometry(10,10,650,970)
        self.scene=QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 640, 960)
        self.setScene(self.scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)

        self.setWindowTitle('Main')
        self.show()
        
    def closeEvent(self, event):
        print 'closeEvent'

        self.settings = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('MainWindow')
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.endGroup()

### ListWindow
class ListWindow(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(ListWindow, self).__init__(parent)
        self.initUI()
        self.loadSetting()
     
    def loadSetting(self):
        print 'loadSetting'
        self.settings = QtCore.QSettings('setting.ini', QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('ListWindow')
            geometry=self.settings.value('geometry')
            if (geometry != None):
                self.restoreGeometry(geometry)
            self.settings.endGroup()
    
    def initUI(self):
        print 'initUI'
        self.model=QtGui.QStandardItemModel(0,11)
        
        self.model.setHeaderData(0,QtCore.Qt.Horizontal, u'filename')
        self.model.setHeaderData(1,QtCore.Qt.Horizontal, u'frame')
        self.model.setHeaderData(2,QtCore.Qt.Horizontal, u'magid')
        self.model.setHeaderData(3,QtCore.Qt.Horizontal, u'scanid')
        self.model.setHeaderData(4,QtCore.Qt.Horizontal, u'widthX')
        self.model.setHeaderData(5,QtCore.Qt.Horizontal, u'widthY')
        self.model.setHeaderData(6,QtCore.Qt.Horizontal, u'centerX')
        self.model.setHeaderData(7,QtCore.Qt.Horizontal, u'centerY')
        self.model.setHeaderData(8,QtCore.Qt.Horizontal, u'score')
        self.model.setHeaderData(9,QtCore.Qt.Horizontal, u'dic')
        self.model.setHeaderData(10,QtCore.Qt.Horizontal, u'Y')
        
#        i=0
#        self.model.setItem(i, 0, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 1, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 2, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 3, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 4, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 5, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 6, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 7, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 8, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 9, QtGui.QStandardItem('-'))
#        self.model.setItem(i, 10, QtGui.QStandardItem('-'))

        self.setModel(self.model)
        self.setWindowTitle('List')
        self.show()
        
    def closeEvent(self, event):
        print 'closeEvent'
        self.settings = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('ListWindow')
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.endGroup()

    def setItem(self, waku):
        global wakulist
        
        i = ListWin.model.rowCount()
        self.model.setItem(i, 0, QtGui.QStandardItem(waku['filename'][0]))
        self.model.setItem(i, 1, QtGui.QStandardItem(waku['frame'][0]))
        self.model.setItem(i, 2, QtGui.QStandardItem(waku['magid'][0]))
        self.model.setItem(i, 3, QtGui.QStandardItem(waku['scanid'][0]))
        self.model.setItem(i, 4, QtGui.QStandardItem(waku['widthX'][0]))
        self.model.setItem(i, 5, QtGui.QStandardItem(waku['widthY'][0]))
        self.model.setItem(i, 6, QtGui.QStandardItem(waku['centerX'][0]))
        self.model.setItem(i, 7, QtGui.QStandardItem(waku['centerY'][0]))
        self.model.setItem(i, 8, QtGui.QStandardItem('-'))
        self.model.setItem(i, 9, QtGui.QStandardItem('-'))
        self.model.setItem(i, 10, QtGui.QStandardItem('-'))

### GraphWindow
class GraphWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GraphWindow, self).__init__(parent)
        self.initUI()
        self.loadSetting()

    def loadSetting(self):
        print 'loadSetting'
        self.settings = QtCore.QSettings('setting.ini', QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('GraphWindow')
            geometry=self.settings.value('geometry')
            if (geometry != None):
                self.restoreGeometry(geometry)
            self.settings.endGroup()
        
    def initUI(self):
#        # 日本語を使うため必要
#        fontprop = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/fonts-japanese-gothic.ttf")        

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)

        self.axes.clear()
        self.axes.grid(True)
        
#        self.axes.bar()
        
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.canvas, 0, 0)

        self.setLayout(self.grid)
        self.setWindowTitle('Graph')
        self.show()
    
    def closeEvent(self, event):
        print 'closeEvent'

        self.settings = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('GraphWindow')
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.endGroup()
    
### InputWindow
class InputWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(InputWindow, self).__init__(parent)
        self.initUI()
        self.loadSetting()

    def loadSetting(self):
        print 'loadSetting'
        self.settings = QtCore.QSettings('setting.ini', QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('InputWindow')
            geometry=self.settings.value('geometry')
            if (geometry != None):
                self.restoreGeometry(geometry)
                
            self.settings.endGroup()
        
    def initUI(self):
        print 'initUI'
        grid = QtGui.QGridLayout()
        layout = 0
        
        ### File
        global fileProgressBar        
        
        self.file=QtGui.QLabel('file')

        self.fileEdit=QtGui.QComboBox()
        self.fileEdit.addItem('******** all ********')
        self.fileEdit.activated.connect(self.chengeFile)

        self.fileOpenBtn=QtGui.QPushButton('Open AVI file...')
        self.fileOpenBtn.clicked.connect(self.fileOpenBtn_Onclick)

        fileProgressBar=QtGui.QProgressBar()
        fileProgressBar.setRange(0,100)
        fileProgressBar.setValue(0)

        grid.addWidget(self.file, layout, 0)
        grid.addWidget(self.fileEdit, layout, 1)
        grid.addWidget(self.fileOpenBtn, layout, 2)
        grid.addWidget(fileProgressBar, layout, 3)
        layout = layout + 1

        ### Frame
        self.frame=QtGui.QLabel('Frame')
        self.frameEdit=QtGui.QComboBox()
        self.frameEdit.addItem('all')
        self.framePreBtn=QtGui.QPushButton('<')
        self.framePreBtn.clicked.connect(self.framePreBnt_Onclick)
        self.frameNextBtn=QtGui.QPushButton('>')
        grid.addWidget(self.frame, layout, 0)
        grid.addWidget(self.frameEdit, layout, 1)
        grid.addWidget(self.framePreBtn, layout, 2)        
        grid.addWidget(self.frameNextBtn, layout, 3)
        layout = layout + 1        
        
        ### Dic
        self.dic=QtGui.QLabel('Dic')
        self.dicEdit=QtGui.QComboBox()
        
        self.dicEdit.addItem('all')
        for d in ['64x128', '32x64']:
            self.dicEdit.addItem(d)

        grid.addWidget(self.dic, layout, 0)
        grid.addWidget(self.dicEdit, layout, 1)
        layout = layout + 1        
        
        ### Height
        self.height=QtGui.QLabel('Height')
        self.heightEdit=QtGui.QComboBox()
        
        self.heightEdit.addItem('all')
        for h in ['80', '90', '100', '110', '120', '130', '140', '150', '160', '170', '180', '190', '200']:
            self.heightEdit.addItem(h)
        
        grid.addWidget(self.height, layout,0)
        grid.addWidget(self.heightEdit, layout,1)
        layout = layout + 1        

#        ### close
#        self.closeBtn=QtGui.QPushButton('Close')
#        self.closeBtn.clicked.connect(self.closeBtn_Onclick)
#        grid.addWidget(self.closeBtn, layout, 3)        
#        layout = layout + 1

        ### 保存
        self.saveImgBtn=QtGui.QPushButton('SaveImage')
        grid.addWidget(self.saveImgBtn, layout, 3)
        layout = layout + 1
        
        self.setLayout(grid)
        self.setWindowTitle('Input')
        self.show()
    
    def closeEvent(self, event):
        print 'closeEvent'
        self.settings = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
        if self.settings != None:
            self.settings.beginGroup('InputWindow')
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.endGroup()

    def chengeFile(self):
            print 'changeFile'
            print self.fileEdit.currentText()

    def fileOpenBtn_Onclick(self):
        print 'fileOpenBtn clicked'
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '')

        if Analyze(filename) == True:
            print filename
            self.fileEdit.addItem(filename)
        else:
            QtGui.QMessageBox.warning(self, 'Test', u'Test')

    def framePreBnt_Onclick(self):
        print 'framePreBtn clicked'
    
    def frameNextBnt_Onclick(self):
        print 'frameNextBtn clicked'
    
    def closeBtn_Onclick(self):
        print 'closeBtn clicked'
    
### main
def main():
    global IptWin
    global MainWin
    global ListWin
    global GraphWin
    global wakulist
    
    app = QtGui.QApplication(sys.argv)
    
    IptWin=InputWindow() 
    MainWin=MainWindow()
    ListWin=ListWindow()
    GraphWin=GraphWindow()
    wakulist =pd.DataFrame()

    app.exec_()

if __name__ == '__main__':
    main()
