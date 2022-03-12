#!/usr/bin/env python3
# *_* coding : UTF-8 *_*
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QDialog,QTabWidget
from PyQt5.QtCore import *
from Logic_CommonHelper import ConfigHelper
from Logic_SetTab1 import SetTab1
from Logic_SetTab2 import SetTab2
from Logic_SetTab3 import SetTab3




class SetFrom(QDialog):
    
    def __init__(self,parent):
        super(SetFrom,self).__init__(parent)
        self.setWindowTitle('设置')
        self.TabFrom=TabFrom(self)
        
        self.adjustSize()

    
    def __call__(self,SIGNAL) :
        SIGNAL.connect(self.open)
        

    def open(self):
        self.exec_()
        
        
class TabFrom(QTabWidget):
    def __init__(self,parent):
        super(TabFrom,self).__init__(parent)
        self.father=parent
        self.setUsesScrollButtons(False)
        # self.resize(409,311)
        #创建3个选项卡
        self.tab1=QWidget(self)
        self.tab2=QWidget(self)
        self.tab3=QWidget(self)
        # self.tab4=QWidget(self)
        #把三个选项卡添加到栏目中
        self.addTab(self.tab1,'宠物管理')
        self.addTab(self.tab2,'添加动作')
        self.addTab(self.tab3,'B站直播设置')
        # self.addTab(self.tab4,'关于')
        #添加每个选项卡的内容
        self.tabUI=SetTab1(self.tab1)
        self.tabUI2=SetTab2(self.tab2)
        self.tabUI3=SetTab3(self.tab3)
        # self.tabUI4(self.tab4)
        self.currentChanged.connect(self.tabChanged)
        self.adjustSize()
        
    def tabChanged(self,num):
        if num==1:
            self.tabUI2.loadModel(self.tabUI2.modelchoiceBox)
    




if __name__ == '__main__':
    from Logic_Tray import *
    #实例化窗口对象
    app = QApplication(sys.argv)
    #实例化一个主窗口
    win = QWidget()
    win.resize(300,500)
    tp=tray(win)
    #显示窗体
    win.show()
    win2=SetFrom(win)
    # win2(tp.SetForm)
    win2.open()
    
    
    

    #打开消息循环
    sys.exit(app.exec_())