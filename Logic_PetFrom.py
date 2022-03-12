from PyQt5.QtWidgets import QLabel,QWidget,QHBoxLayout,QMenu,QAction,qApp,QDialog,QMessageBox,QApplication
from PyQt5.QtGui import QMovie,QCursor,QPainter,QPainterPath,QBrush,QColor
from PyQt5.QtCore import QPoint,Qt,QRect,QUrl,pyqtSignal
from PyQt5.QtMultimedia import QSoundEffect
from Logic_CommonHelper import ConfigHelper,ModelPath,SoundPath,IconPath,CommonHelper
from ast import literal_eval
from Logic_Tray import *
import sys

#建立宠物数据模型
class PetModel:
    __slots__='url','speed','sound','actionName'
    def __init__(self,petname,petDict:dict):
        if 'url' in petDict:
            self.url=str(ModelPath/petname/petDict.get('url'))
        if 'sound' in petDict:
            if petDict.get('sound')!='':
                self.sound=str(SoundPath(petname)/petDict.get('sound'))
        if 'speed' in petDict:
            self.speed=petDict.get('speed')
        if 'actionName' in petDict:
            self.actionName=petDict.get('actionName')
    


class Pet(QWidget):
    __slots__='gif','config','petname','pets','pet','media','actionName','action','frameCount','rightMenu','gifLabel','is_follow_mouse'
    def __init__(self,parent=None):
        super(Pet,self).__init__(parent)
        #初始化窗口透明,无填充，无头部
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #初始化是否跟随鼠标设置为False防止报错
        self.is_follow_mouse = False
        #读取配置文件，获取当前宠物名
        self.config=ConfigHelper()
        self.petname=self.config.iniFile.get('systemSetting','petname')
        #获取宠物数据,字典类型
        self.pet=PetModel(self.petname,self.config.getItemOtype('pets',self.petname))
        self.media=QSoundEffect()
        self.gifLabel=QLabel(self)
        self.showPet(self.pet)
        self.rightMenu=RightMenuWidget(self)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda:self.rightMenu())  # 开放右键策略
        
        
    #显示宠物，是否循环
    def showPet(self,petData:dict,ToLoop=True):
        #防止连续切换导致的错误
        self.media.stop()
        #实例化一个Qmoive对象
        self.gif=QMovie(petData.url)
        self.gifLabel.setMovie(self.gif)
        self.gif.start()
        self.gif.setSpeed(int(petData.speed))
        try:
            self.media.setSource(QUrl.fromLocalFile(petData.sound))
            self.media.play()
        except:
            pass
        curp=self.gif.currentPixmap()
        self.gifLabel.resize(curp.size())
        self.checkGifloop(ToLoop)
        self.adjustSize()
        
    #通过call方法执行动作
    def __call__(self,action:str):
        print(action)
        modelAction=self.petname+'_action'
        self.action=PetModel(self.petname,self.config.getItemOtype(modelAction,action))
        self.showPet(self.action,False)
        
    def ChangePet(self,petName):
        print(petName)
        self.petname=petName
        self.pet=PetModel(self.petname,self.config.getItemOtype('pets',petName))
        self.showPet(self.pet)
        self.config.add('systemSetting','petname',petName)
        
        
    #判断gif循环状态
    def checkGifloop(self,ToLoop:bool):
        #获取gif循环状态
        loop=self.gif.loopCount()
        #获取gif帧数
        self.frameCount=self.gif.frameCount()
        if ToLoop:
            if loop==0:
                self.gif.frameChanged.connect(self.GifToLoop)
        else:
            if loop==-1:
                self.gif.frameChanged.connect(self.GifNotToLoop)
            else:
                self.gif.finished.connect(lambda:self.showPet(self.pet))
    
    def GifToLoop(self,frameNum):
        if self.frameCount-1==frameNum:
            self.gif.jumpToFrame(0)
            self.gif.start()
    def GifNotToLoop(self,frameNum):
        if self.frameCount-1==frameNum:
            self.gif.stop()
            self.showPet(self.pet)
            
    #鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
	#鼠标移动, 则宠物也移动
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()
	#鼠标释放时, 取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 添加中文的确认退出提示框
    def closeEvent(self, event):
        # 创建一个消息盒子（提示框）
        quitMsgBox = QMessageBox(self)
        # 设置提示框的标题
        quitMsgBox.setWindowTitle('确认提示')
        # 设置提示框的内容
        quitMsgBox.setText('你确认退出吗？')
        # 设置按钮标准，一个yes一个no
        quitMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 获取两个按钮并且修改显示文本
        buttonY = quitMsgBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = quitMsgBox.button(QMessageBox.No)
        buttonN.setText('取消')
        quitMsgBox.exec_()
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if quitMsgBox.clickedButton() == buttonY:
            sys.exit(0)
        else:
            event.ignore()
    #在画面渲染前添加事件
    def showEvent(self,event):
        pass
            

#右键菜单 Qt.FramelessWindowHint | Qt.Popup 设置无边框 事件冒泡
class RightMenuWidget(QMenu):
    SetFromShow=pyqtSignal(bool)
    __slots__='hideAction','outAction','config','setAction','actionSection','actionOptions'
    def __init__(self, parent) :
        super(RightMenuWidget,self).__init__(parent)
        self.actionSection=parent.petname+'_action'
        self.config=ConfigHelper()
        self.transparentBg(self)
        self.setUpUI(parent)
    
    #添加右键菜单
    def setUpUI(self,parent):
        self.setAction=QAction('设置',self,triggered=lambda:self.SetFromShow.emit(True))
        self.hideAction=QAction('隐藏', self, triggered=lambda:parent.hide())
        self.outAction=QAction('退出', self, triggered=parent.close)
        self.addAction(self.setAction)
        self.addPetsMenu(self.parent())
        self.actionMenu(self.parent())
        self.addAction(self.hideAction)
        self.addAction(self.outAction)
    
    #添加宠物二级菜单
    def addPetsMenu(self,parent):
        secMenu=self.addMenu('宠物')
        self.transparentBg(secMenu)
        try:
            self.pets=self.config.iniFile.options('pets')
            if self.pets !=[]:
                for item in self.pets:
                    secMenu.addAction(QAction(item,self,triggered=lambda check,index=item:parent.ChangePet(index)))
        except:
            secMenu.addAction('空')
    
    #添加动作二级菜单
    def actionMenu(self,parent):
            secMenu=self.addMenu('动作')
            self.transparentBg(secMenu)
            try:
                self.actionOptions=self.config.iniFile.items(self.actionSection)
                if self.actionOptions !=[]:
                    for index,item in self.actionOptions:
                        item=literal_eval(item)
                        secMenu.addAction(QAction(item.get('actionName'),self,triggered=lambda  check, index=index:parent(index)))
            except:
                secMenu.addAction('空')
                
    #去除wdiget背景
    def transparentBg(self,item):
            item.setAttribute(Qt.WA_TranslucentBackground, True)
            item.setAutoFillBackground(False)
            item.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
    
    def __call__(self):
        self.exec_(QCursor.pos())
        








if __name__=='__main__':
    app=QApplication(sys.argv)
    qssStyle = CommonHelper.readQss()
    win=Pet()
    # l('action1')
    win.setStyleSheet(qssStyle)
    mtray=tray(win)
    sc=Screens()
    sc.GetPos(win)
    win.show()
    sys.exit(app.exec())
