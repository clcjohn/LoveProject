#!/usr/bin/env python3
# *_* coding : UTF-8 *_*

import sys,os
from pathlib import Path
from ast import literal_eval
from PyQt5.QtCore import QFile, QSize, Qt
from PyQt5.QtGui import QIcon, QMovie,QCursor
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QFrame, QHBoxLayout, QLabel, QLineEdit,QDialog,
                             QMessageBox, QPushButton, QSizePolicy,
                             QSpacerItem, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget,QHeaderView,QAbstractItemView,QItemDelegate)
from Logic_CommonHelper import ProjectPath,ConfigHelper,ModelPath,SoundPath,DeskTopPath




class SetTab2(QWidget):
    def __init__(self,parent):
        super(SetTab2,self).__init__(parent)
        self.setupUI(parent)
        self.setFixedSize(QSize(495,300))
        # #事件绑定
        self.addButton.clicked.connect(lambda:self.addTableLine())
        self.cancel.clicked.connect(lambda:self.cancel_button())
        #加载Combobox数据绑定信号到列表
        self.loadModel(self.modelchoiceBox)
        self.OKbutton.clicked.connect(lambda:self.tableWidget.OkButtonClick())
        self.delbutton.clicked.connect(lambda:self.tableWidget.deleteRow())
    #初始化界面
    def setupUI(self,parent):
        parent.setContentsMargins(0,0,0,0)
        #创建水平和垂直载体
        verticalLayout_1 = QVBoxLayout(parent)
        verticalLayout_1.setContentsMargins(0, 10, 0, 10)
        horizontalLayout = QHBoxLayout()
        horizontalLayout_2 = QHBoxLayout()
        #创建按钮
        modelchoiceLabel = QLabel('选择模型',parent)
        self.modelchoiceBox = QComboBox(parent)
        horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #添加数据列表
        self.tableWidget = ActionTable(parent)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addButton = QPushButton('添加',parent)
        self.delbutton=QPushButton('删除',parent)
        self.OKbutton = QPushButton('保存',parent)
        self.cancel = QPushButton('取消',parent)
        #添加按钮到载体
        horizontalLayout.addWidget(modelchoiceLabel)
        horizontalLayout.addWidget(self.modelchoiceBox)
        horizontalLayout.addItem(horizontalSpacer_1)
        verticalLayout_1.addLayout(horizontalLayout)
        verticalLayout_1.addWidget(self.tableWidget)
        horizontalLayout_2.addItem(horizontalSpacer)
        horizontalLayout_2.addWidget(self.addButton)
        horizontalLayout_2.addWidget(self.delbutton)
        horizontalLayout_2.addWidget(self.OKbutton)
        horizontalLayout_2.addWidget(self.cancel)
        verticalLayout_1.addLayout(horizontalLayout_2)
    #添加按钮点击事件
    def addTableLine(self):
        self.tableWidget.add()
    #取消按钮点击事件
    def cancel_button(self):
        self.nativeParentWidget().close()
    
    #载入模型名称
    def loadModel(self,QComboBox):
        QComboBox.clear()
        config=ConfigHelper()
        self.pets=config.iniFile.options('pets')
        QComboBox.addItems(self.pets)
        #初始化一次列表加载model内容
        self.tableWidget.loadline(self.modelchoiceBox.currentText())
        self.modelchoiceBox.activated.connect(lambda:self.tableWidget.loadline(self.modelchoiceBox.currentText()))
        
#动作列表
class ActionTable(QTableWidget):
    __slots__ ='id','tablist','rowlist','acionName','petActions','petActionList','petname'
    def __init__(self,parent):
        super(ActionTable,self).__init__(parent)
        self.QCheckBoxList,self.petActions,self.rowlist,self.petActionList=[],[],[],[]
        self.fileUrl=''
        self.setSelectionBehavior(1)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setFixedHeight(20) ##设置表头高度
        self.setColumnCount(5)##设置表格一共有五列
        self.setHorizontalHeaderLabels(['选择','动作','声音','播放速度','动作名称'])#设置表头文字
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.doubleClicked.connect(lambda:self.OpenFile())
        self.setMouseTracking(True)
        self.cellClicked.connect(self.RowIsChecked)
        
    #添加选择框选中事件
    def checkboxSelect(self,checkstate,checkbox_obj):
        id=self.QCheckBoxList.index(checkbox_obj)
        if checkstate:
            self.rowlist.append(id)
            print(self.rowlist)
        else:
            self.rowlist.remove(id)
        
    #绑定复选框和第一列，点击第一列则选中复选框，反之则取消选择
    def RowIsChecked(self,row,column):
        if column==0 and self.QCheckBoxList[row].checkState()==0:
            self.QCheckBoxList[row].setCheckState(2)
            self.rowlist.append(row)
            print(self.rowlist)
        elif column==0:
            self.QCheckBoxList[row].setCheckState(0)
            self.rowlist.remove(row)
            print(self.rowlist)

    #添加一行
    def add(self):
        newDict={'url':'','sound':'','speed':100,'actionName':''}
        newmodel=ActionTableModel(newDict)
        self.LineModel(newmodel)
    
    #读取选中的宠物的动作列表
    def loadline(self,petname):
        #清空表格中的数据，加载配置文件内容
        self.rowlist.clear()
        self.petActionList.clear()
        self.QCheckBoxList.clear()
        self.clearContents()
        self.setRowCount(0)
        #读取配置文件,根据选择获取当前模型下的所有动作
        config=ConfigHelper()
        self.petname=petname
        self.actionName=petname+'_action'
        try:
            self.petActions=config.iniFile.items(self.actionName)
            for item in self.petActions:
                self.petActionList.append(ActionTableModel(item))
            for item in self.petActionList:
                self.LineModel(item)
        except:
            config.iniFile.add_section(self.actionName)
    
    #添加行模型
    def LineModel(self,actionModel):
            row=self.rowCount()
            #添加新的一行
            self.setRowCount(row+1)
            self.TCheckBoxCreate(row)
            action=QTableWidgetItem(actionModel.url)
            action.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            self.setItem(row,1,action)
            sound=QTableWidgetItem(actionModel.sound)
            sound.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            self.setItem(row,2,sound)
            speed=QTableWidgetItem(str(actionModel.speed))
            speed.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
            self.setItem(row,3,speed)
            actionName=QTableWidgetItem(actionModel.actionName)
            actionName.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
            self.setItem(row,4,actionName)
    
        #添加选择框
    def TCheckBoxCreate(self,row):
        w=QWidget(self)
        h=QHBoxLayout(w)
        h.setAlignment(Qt.AlignCenter)
        checkbox=QCheckBox(w)
        self.QCheckBoxList.append(checkbox)
        checkbox.clicked.connect(lambda checkstate,checkbox_obj=checkbox:self.checkboxSelect(checkstate,checkbox_obj))
        h.addWidget(checkbox)
        w.setLayout(h)
        self.setCellWidget(row,0,w)
    
    #添加文件事件
    def OpenFile(self):
        if self.currentItem() != None:
            current_item=self.currentItem()
            if current_item.column()==1:
                self.fileUrl,filetype = QFileDialog.getOpenFileName(self, "Open", DeskTopPath, "*.gif;;All Files(*)")
            elif current_item.column()==2:
                self.fileUrl,filetype = QFileDialog.getOpenFileName(self, "Open", DeskTopPath, "*.wav;;All Files(*)")
            if self.fileUrl !='':
                current_item.setText(Path(self.fileUrl).name)
                current_item.setToolTip(self.fileUrl)

    #确定按钮
    def OkButtonClick(self):
        data=[]
        #创建文件操作对象
        row=self.rowCount()
        #循环获取当前所有行里的数据
        for i in range(row):
            actiondict={'url':'','sound':'','speed':'','actionName':''}
            actiondict['url']=self.item(i,1).text()
            self.SavePathToRes(self.item(i,1).text())
            actiondict['sound']=self.item(i,2).text()
            self.SavePathToRes(self.item(i,2).text(),1)
            actiondict['speed']=self.item(i,3).text()
            actiondict['actionName']=self.item(i,4).text()
            data.append(actiondict)
        #把数据存进配置文件
        f=ConfigHelper()
        try:
            for index,item in enumerate(data):
                option='action'+str(index+1)
                f.add(self.actionName,option,str(item))
            QMessageBox.warning(self,'成功','保存完成！')
        except:
            QMessageBox.warning(self,'错误','保存失败！')

    def SavePathToRes(self,item,PathType:int=0):
        if self.petname !='' and self.fileUrl !='':
            if PathType==0:
                path=ModelPath/self.petname/item
            else:
                path=SoundPath(self.petname)/item
            curFile=QFile(self.fileUrl)
            curFile.copy(str(path))
        else:
            pass
                
    
    
    #删除行
    def deleteRow(self):
        #降序排列
        self.rowlist.sort(reverse = True)
        #根据rowlist循环删除行和复选框
        for item in self.rowlist:
            self.isDataInLine(item)
            self.removeRow(item)
            del self.QCheckBoxList[item]
        self.rowlist.clear()
        QMessageBox.warning(self,'成功','删除成功！')

    def isDataInLine(self,row):
        f=ConfigHelper()
        action='action'+str(row)
        try:
            print(f.iniFile.has_option(self.actionName,action))
            if f.iniFile.has_option(self.actionName,action):
                f.remove_option(self.actionName,action)
        except:
            return None
    
#动作列表模型
class ActionTableModel:
    __slots__='url','sound','speed','actionName','action'
    def __init__(self,ActionData):
        if isinstance(ActionData,dict):
            actionDict=ActionData
        else:
            self.action=ActionData[0]
            actionDict=literal_eval(ActionData[1])
        self.url=actionDict.get('url')
        self.sound=actionDict.get('sound')
        self.speed=actionDict.get('speed')
        self.actionName=actionDict.get('actionName')
    
    

if __name__ == '__main__':
    from PyQt5.QtWidgets import QTabWidget

    #实例化窗口对象
    app = QApplication(sys.argv)
    #实例化一个主窗口
    win = QWidget()
    tabwin=QTabWidget(win)

    tabitem=QWidget(tabwin)
    set_tab1=SetTab2(tabitem)
    tabwin.addTab(tabitem,'ceshi')
    #显示窗体
    win.show()
    tabitem.adjustSize()
    tabwin.adjustSize()
    win.adjustSize()
    #打开消息循环
    sys.exit(app.exec_())
