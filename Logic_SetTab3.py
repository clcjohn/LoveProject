#!/usr/bin/env python3
# *_* coding : UTF-8 *_*
from PyQt5.QtWidgets import QWidget,QLineEdit,QVBoxLayout,QLabel,QHBoxLayout,QPushButton,QSpacerItem,QSizePolicy,QMessageBox
from Logic_CommonHelper import ConfigHelper




class SetTab3(QWidget):
    __slots__='roomNum','config'
    def __init__(self,parent=None) :
        super(SetTab3,self).__init__(parent)
        self.config=ConfigHelper()
        self.setupUI(parent)
        self.LoadConfig()
        self.OkButton.clicked.connect(self.OK)
        
    def setupUI(self,parent):
        verticalLayout_1=QVBoxLayout(parent)
        roomNumText=QLabel(parent)
        roomNumText.setText('房间号')
        self.roomNum=QLineEdit(parent)
        self.roomNum.setPlaceholderText('请输入B站房间号')
        horizontalLayout1=QHBoxLayout()
        horizontalLayout1.addWidget(roomNumText)
        horizontalLayout1.addWidget(self.roomNum)
        
        horizontalLayout2=QHBoxLayout()
        timeIntervalText=QLabel(parent)
        timeIntervalText.setText('监测频率')
        self.timeInterval=QLineEdit(parent)
        self.timeInterval.setPlaceholderText('以秒为单位，不建议太频繁的获取！！！')
        horizontalLayout2.addWidget(timeIntervalText)
        horizontalLayout2.addWidget(self.timeInterval)
        
        horizontalLayout3=QHBoxLayout()
        self.OkButton=QPushButton('确定',parent)
        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        horizontalLayout3.addItem(verticalSpacer)
        horizontalLayout3.addWidget(self.OkButton)
        
        verticalLayout_1.addItem(horizontalLayout1)
        verticalLayout_1.addItem(horizontalLayout2)
        verticalLayout_1.addItem(horizontalLayout3)
    
    def LoadConfig(self):
        roomid=self.config.iniFile.get('BiliBili','roomid')
        timeInterval=self.config.iniFile.get('BiliBili','timeInterval')
        self.roomNum.setText(roomid)
        self.timeInterval.setText(timeInterval)
        

    def OK(self):
        roomid=self.roomNum.text()
        timeInterval=self.timeInterval.text()
        try:
            self.config.add('BiliBili','roomid',roomid)
            self.config.add('BiliBili','timeInterval',timeInterval)
            QMessageBox.information(self.parent(), '通知', '保存完成！')
        except:
            QMessageBox.information(self.parent(), '通知', '保存失败！')






if __name__=='__main__':
    from PyQt5.QtWidgets import QTabWidget,QApplication
    import sys

    #实例化窗口对象
    app = QApplication(sys.argv)
    #实例化一个主窗口
    win = QWidget()
    tabwin=QTabWidget(win)
    tabitem=QWidget(tabwin)
    set_tab3=SetTab3(tabitem)
    tabwin.addTab(tabitem,'ceshi')

    
    #显示窗体
    win.show()
    win.adjustSize()
    #打开消息循环
    sys.exit(app.exec_())