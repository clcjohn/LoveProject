#!/usr/bin/env python3
# *_* coding : UTF-8 *_*
import sys
from ast import literal_eval
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import QFile, QSize,Qt,pyqtSignal
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog, QFrame,QDialog,QAbstractItemView,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from Logic_CommonHelper import CommonHelper, ConfigHelper, ModelPath, DeskTopPath,FileHandle


class SetTab1(QWidget):
    __slots__ ='petTable','addPet','delPet','modifyPet','PetAddFrom'
    def __init__(self,parent):
        super(SetTab1,self).__init__(parent)
        #添加ui布局
        self.setupUI(parent)
        self.setFixedSize(QSize(320,300))
        #绑定事件
        self.BindingControl(parent)

    def setupUI(self,parent):
        verticalLayout_1=QVBoxLayout(parent)
        self.petTable=PetTable(parent)
        horizontalLayout1=QHBoxLayout()
        self.addPet=QPushButton('添加',parent)
        self.delPet=QPushButton('删除',parent)

        
        verticalLayout_1.addWidget(self.petTable)
        horizontalLayout1.addWidget(self.addPet)
        horizontalLayout1.addWidget(self.delPet)
        verticalLayout_1.addItem(horizontalLayout1)
        self.PetAddFrom=PetAdd(self)
        
    def BindingControl(self,parent):    
        self.addPet.clicked.connect(self.PetAddFrom.exec_)
        self.PetAddFrom.PetAddFinished.connect(self.petTable.loadline)
        self.delPet.clicked.connect(self.petTable.PetDeleted)



class PetTable(QTableWidget):
    __slots__ ='config','petname','pets','petsList','QCheckBoxList','rowlist'
    def __init__(self,parent):
        super(PetTable,self).__init__(parent)
        self.pets,self.petsList,self.rowlist,self.QCheckBoxList=[],[],[],[]
        #table基础设置
        self.setSelectionBehavior(1)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setFixedHeight(20) ##设置表头高度
        self.setColumnCount(3)##设置表格一共有五列
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(['选择','宠物名称','播放速度'])#设置表头文字
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #加载数据
        self.loadline()
        #绑定事件
        self.cellClicked.connect(self.RowIsChecked)
        
    
    #加载数据    
    def loadline(self,reload=True):
        if reload:
            self.QCheckBoxList.clear()
            self.petsList.clear()
            self.pets.clear()
            self.rowlist.clear()
            #清空表格，准备填入数据
            self.clearContents()
            self.setRowCount(0)
            #读取配置文件
            self.config=ConfigHelper()
            #获取配置文件中所有的宠物
            try:
                self.pets=self.config.iniFile.items('pets')
                # print(self.pets,type(self.pets))
                for item in self.pets:
                    self.petsList.append(PetTableModel(item))
                # print(self.petsList)
                # print(self.petsList[0].petname)
                for item in self.petsList:
                    self.LineModel(item.petname,item.speed)
            except:
                pass
        
    #添加空行
    def addLine(self,parent=None):
        self.LineModel()

    def LineModel(self,args1='',args2=''):
        row=self.rowCount()
        self.setRowCount(row+1)
        # print(row)
        self.TCheckBoxCreate(row)
        name=QTableWidgetItem(args1)
        name.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.setItem(row,1,name)
        speed=QTableWidgetItem(str(args2))
        speed.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        self.setItem(row,2,speed)
    
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

    #添加选择框选中事件
    def checkboxSelect(self,checkstate,checkbox_obj):
        id=self.QCheckBoxList.index(checkbox_obj)
        if checkstate:
            self.rowlist.append(id)
        else:
            self.rowlist.remove(id)
        
    
    #绑定复选框和第一列，点击第一列则选中复选框，反之则取消选择
    def RowIsChecked(self,row,column):
        if column==0 and self.QCheckBoxList[row].checkState()==0:
            self.QCheckBoxList[row].setCheckState(2)
            self.rowlist.append(row)
        elif column==0:
            self.QCheckBoxList[row].setCheckState(0)
            self.rowlist.remove(row)
            
    #删除事件
    def PetDeleted(self):
        #判断行有没被选中
        if len(self.rowlist)>0:
            # 创建一个消息盒子（提示框）
            delMsgBox = QMessageBox(self)
            # 设置提示框的标题
            delMsgBox.setWindowTitle('确认提示')
            # 设置提示框的内容
            delMsgBox.setText('你确认要删除这些吗？如果删除将会连数据一起删除')
            # 设置按钮标准，一个yes一个no
            delMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # 获取两个按钮并且修改显示文本
            buttonY = delMsgBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            buttonN = delMsgBox.button(QMessageBox.No)
            buttonN.setText('取消')
            delMsgBox.exec_()
            # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
            if delMsgBox.clickedButton() == buttonY:
                #删除行内容
                self.rowlist.sort(reverse = True)
                removePet=[]
                for row in self.rowlist:
                    #获取要删除的宠物名称
                    removePet_name=self.item(row,1)
                    removePet.append(removePet_name.text())
                    #删除行
                    self.removeRow(row)
                    del self.QCheckBoxList[row]
                self.rowlist.clear()
                #删除数据
                self.removePetData(removePet)
                QMessageBox.warning(self,'成功','删除成功！')
            else:
                pass
        else:
            QMessageBox.warning(self,'错误','你行没有选择目标！')
            
    #删除数据      
    def removePetData(self,DataList:list):
        config=ConfigHelper()
        try:
            for item in DataList:
                #删除本地文件
                locationPath=ModelPath/item
                try:
                    locationPath.rmdir()
                except:
                    #清空改宠物文件夹内文件
                    FileHandle.LocationPath_dirDel(locationPath)
                    locationPath.rmdir()
                config.remove_option('pets',item)
                config.remove_section(item+'_action')
        except:
            pass
    

            
            
        
#宠物表格模型
class PetTableModel:
    __slots__='url','speed','petname'
    def __init__(self,petData:Tuple):
        self.petname=petData[0]
        petdict=literal_eval(petData[1])
        self.url=petdict.get('url')
        self.speed=petdict.get('speed')
        
#添加宠物弹窗
class PetAdd(QDialog):
    PetAddFinished=pyqtSignal(bool)
    __slots__ ='config','gif_preview','gif_speed','previewSource','addPet','speedSet','newPetNameSet','petname','cur_pet','pets'
    def __init__(self,parent):
        super(PetAdd,self).__init__(parent)
        self.config=ConfigHelper()
        self.petname=self.config.iniFile.get('systemSetting','petname')
        self.cur_pet=self.config.getItemOtype('pets',self.petname)
        self.previewSource=QMovie()
        #添加ui布局
        self.setupUI()
        #绑定事件
        self.BindingEvent(parent)

    def setupUI(self):
        self.setContentsMargins(0,0,0,0)
        # parent.setGeometry(QRect(0, 0, 412, 319))
        #定义水平布局
        horizontalLayout1=QHBoxLayout(self)
        horizontalLayout1.setContentsMargins(0, 10, 0, 10)
        #获取初始化预览图
        self.gif_preview=QLabel(self)
        self.gif_preview.setFixedSize(QSize(150, 300))
        self.gif_preview.setScaledContents(True)
        self.gif_preview.setMovie(self.previewSource)
        #创建分割线
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        #创建布局
        verticalLayout_1=QVBoxLayout()
        horizontalLayout2 = QHBoxLayout()
        horizontalLayout3 = QHBoxLayout() 
        #添加宠物按钮
        self.addPet = QPushButton('添加宠物',self)
        self.addPet.setAutoDefault(False)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Gif_adress = QLabel('',self)
        #添加速度设置标签
        speed = QLabel('播放速度设置',self)
        speed.setContentsMargins(0,10,0,10)
        self.speedSet = QLineEdit('',self)
        self.speedSet.setToolTip('请输入数值')
        #添加模型名称
        newPetName = QLabel('模组名称',self)
        newPetName.setToolTip('模组名称作为后期绑定动作的重要参数，请好好取名')
        newPetName.setContentsMargins(0,10,0,10)
        self.newPetNameSet = QLineEdit('',self)
        self.newPetNameSet.setToolTip('模组名称作为后期绑定动作的重要参数，请好好取名')
        self.newPetNameSet.setPlaceholderText("后期绑定动作的重要参数")
        #添加确认和取消按钮
        verticalSpacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.OKbutton = QPushButton('确定',self)
        self.cancel = QPushButton('取消',self)
        #添加控件到布局
        horizontalLayout1.addWidget(self.gif_preview)
        horizontalLayout1.addWidget(line)
        horizontalLayout2.addWidget(self.addPet)
        horizontalLayout2.addItem(horizontalSpacer)
        verticalLayout_1.addItem(horizontalLayout2)
        verticalLayout_1.addWidget(self.Gif_adress)
        verticalLayout_1.addWidget(speed)
        verticalLayout_1.addWidget(self.speedSet)
        verticalLayout_1.addWidget(newPetName)
        verticalLayout_1.addWidget(self.newPetNameSet)
        verticalLayout_1.addItem(verticalSpacer)
        horizontalLayout3.addWidget(self.OKbutton)
        horizontalLayout3.addWidget(self.cancel)
        verticalLayout_1.addItem(horizontalLayout3)
        horizontalLayout1.addItem(verticalLayout_1)
        
        
    def BindingEvent(self,parent):
            self.previewSource.setFileName(str(ModelPath/self.petname/self.cur_pet.get('url')))
            self.previewSource.setSpeed(self.cur_pet.get('speed'))
            self.previewSource.start()
            self.speedSet.setText(str(self.cur_pet.get('speed')))
            self.addPet.clicked.connect(self.AddPet)
            self.speedSet.textChanged.connect(lambda:self.GifSpeedSet(self.speedSet.text()))
            self.OKbutton.clicked.connect(lambda:self.Ok_tab1(parent))
            self.cancel.clicked.connect(lambda:self.cancel_button())
        
    #添加宠物按钮
    def AddPet(self):
        self.fileUrl,_ = QFileDialog.getOpenFileName(self, "Open", DeskTopPath, "*.gif;;All Files(*)" )
        if self.fileUrl != "":  # “”为用户取消
            self.Gif_adress.setToolTip(self.fileUrl)
            self.Gif_adress.setText(self.charChange(self.fileUrl,25))
            self.fileUrl=Path(self.fileUrl)
            if self.newPetNameSet.text()=='' or self.newPetNameSet.text() == '后期绑定动作的重要参数':#如果用户没有填模型名称，把文件名作为模型名称
                self.newPetNameSet.setText(self.fileUrl.stem)
            self.New_petPerivew(str(self.fileUrl))
            
    #改变预览内容
    def New_petPerivew(self,url):
        if url != '':
            self.previewSource.stop()
            self.previewSource.setFileName(url)
            self.previewSource.start()
            self.previewSource.setSpeed(100)
            self.speedSet.setText('100')
            
            
    #修改显示速度
    def GifSpeedSet(self,speed):
        self.speedSet.setStyleSheet('color:#000')
        if speed.isdigit():
            speed=int(speed)
            self.previewSource.stop()
            self.previewSource.setSpeed(speed)
            self.previewSource.start()
        else:
            self.speedSet.setStyleSheet('color:red')
            self.speedSet.setText('只能输入数字')
            

    #文字超出范围修改
    def charChange(self,Getstring:str,stringlen:int):
        if len(Getstring)>stringlen:
            Getstring='...'+Getstring[stringlen:]
            return Getstring
        
    #取消按钮
    def cancel_button(self):
        self.close()
        
    #确定按钮点击事件,保存数据写入配置文件
    def Ok_tab1(self,parent):
        #判断数据
        if str(self.fileUrl) !='' and self.newPetNameSet.text() !='':
            #文件处理操作
            newpetname=self.newPetNameSet.text()
            save_path=ModelPath/newpetname
            save_path.mkdir(parents = True, exist_ok = True)
            copy_path=str(save_path/newpetname)+str(self.fileUrl.suffix)
            savefile=QFile(str(self.fileUrl))
            savefile.copy(str(copy_path))
            #配置文件数据处理
            saveitemdict=str({'url':self.newPetNameSet.text(),'speed':int(self.speedSet.text())})
            self.config.add('pets',self.newPetNameSet.text(),saveitemdict)
            self.PetAddFinished.emit(True)
            QMessageBox.information(parent, '通知', '保存完成！')
            self.close()
        else:
            self.PetAddFinished.emit(False)
            QMessageBox.information(parent, '通知', '保存失败！')
            self.close()






if __name__ == '__main__':
    from PyQt5.QtWidgets import QTabWidget

    #实例化窗口对象
    app = QApplication(sys.argv)
    #实例化一个主窗口
    win = QWidget()
    tabwin=QTabWidget(win)
    tabitem=QWidget(tabwin)
    set_tab1=SetTab1(tabitem)
    tabwin.addTab(tabitem,'ceshi')

    
    #显示窗体
    win.show()
    win.adjustSize()
    #打开消息循环
    sys.exit(app.exec_())
