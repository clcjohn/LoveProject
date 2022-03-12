from turtle import window_width
from PyQt5.QtWidgets import QSystemTrayIcon,qApp,QMenu,QAction
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie,QIcon
from Logic_CommonHelper import ConfigHelper,ModelPath,SoundPath,IconPath,Screens



class tray(QSystemTrayIcon):
    SetFromShow=pyqtSignal(bool)
    __slots__='config','iconName','tpMenu','tpScMenu','parentWidget','screen','mIcon'
    def __init__(self,parent):
        super(tray,self).__init__(parent)
        self.parentWidget=parent
        self.screen=Screens()
        self.config=ConfigHelper()
        self.iconName=self.config.iniFile.get('systemSetting','tray')
        self.mIcon = QMovie(str(IconPath/self.iconName))  # 用QMovie接收gif图像
        self.mIcon.frameChanged.connect(lambda: self.setIcon(QIcon(self.mIcon.currentPixmap())))
        self.mIcon.start()
        #把鼠标点击图标的信号和槽连接
        self.activated.connect(self.iconClied)
        self.setMenu()
        self.show()
        
    
    #鼠标点击图标事件
    def iconClied(self, reason):
        #"鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            if self.parent().isVisible():
                self.parent().hide()
            else:
                self.parent().show()
    
    def setMenu(self):
        self.tpMenu = QMenu()
        self.setContextMenu(self.tpMenu)
        #菜单动作
        self.OpenSetFrom=QAction('设置',self,triggered=lambda:self.SetFromShow.emit(True))
        self.showSAction1 = QAction("左上", self, triggered=lambda:self.screen.SetFixedPostion(self.parentWidget,'LeftTop'))
        self.showSAction2= QAction("右上",self, triggered=lambda:self.screen.SetFixedPostion(self.parentWidget,'RightTop'))
        self.showSAction3= QAction("左下",self, triggered=lambda:self.screen.SetFixedPostion(self.parentWidget,'LeftBotton'))
        self.showSAction4 = QAction("右下", self, triggered=lambda:self.screen.SetFixedPostion(self.parentWidget,'RightBotton'))
        self.quitAction = QAction("退出", self, triggered=qApp.quit)
        
        #添加菜单
        self.tpScMenu=self.tpMenu.addMenu('位置')
        self.tpMenu.addAction(self.OpenSetFrom)
        self.tpMenu.addSeparator()
        self.tpMenu.addAction(self.quitAction)
        #添加tpScMenu菜单内容
        self.tpScMenu.addAction(self.showSAction1)
        self.tpScMenu.addAction(self.showSAction2)
        self.tpScMenu.addAction(self.showSAction3)
        self.tpScMenu.addAction(self.showSAction4)
        
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow,QApplication
    #实例化窗口对象
    app = QApplication(sys.argv)
    #实例化一个主窗口
    win = QMainWindow()
    #实例化托盘对象
    mtray=tray(win)
    #显示窗体
    win.show()
    #打开消息循环
    sys.exit(app.exec_())