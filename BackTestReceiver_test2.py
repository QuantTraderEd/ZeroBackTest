# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:14:13 2015

@author: assa
"""


from BackTestReceiverThread import BackTestReceiverThread
from PyQt4 import QtGui

class BackTestReciever(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        
        
    def initUI(self):
        self.startPushButton = QtGui.QPushButton('Start', self)
        self.HBoxLayOut = QtGui.QHBoxLayout(self)
        self.HBoxLayOut.addWidget(self.startPushButton)
        self.startPushButton.clicked.connect(self.onClick)
        self.setWindowTitle('BackTestReciever')
        self.resize(240, 50)
        pass
    
    def initThread(self):
        self._thread = BackTestReceiverThread()
        self._thread.finished.connect(self.NotifyThreadEnd)
        pass
    
    
    def onClick(self):
        if not self._thread.isRunning():
            self._thread.start()
            self.startPushButton.setText('Stop')
        else:
            self._thread.stop()
            # self._thread.quit()
            # self._thread.terminate()
            self.startPushButton.setText('Start')
        pass

    
    def NotifyThreadEnd(self):
        self.startPushButton.setText('Start')
        pass
    
    def NotifyMsg(self, row):
        pass
    
    
    def NotifyUpdateImVol(self,df_imvol):        
        xdata = df_imvol['Strike']
        data = df_imvol['ImVol']
        self._OptionVeiwerPlotDlg.plot(xdata, data)
        pass
            
                
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = BackTestReciever()
    wdg.show()
    sys.exit(app.exec_())