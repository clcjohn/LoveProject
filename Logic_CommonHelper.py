#!/usr/bin/env python3
# *_* coding : UTF-8 *_*

from pathlib import Path
import configparser as cp
from ast import literal_eval
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QStandardPaths,QFile



DeskTopPath=(QStandardPaths.standardLocations(QStandardPaths.DesktopLocation))[0]
#获取当前文件目录
ProjectPath=Path.cwd()
#获取资源文件目录
ResourcesPath=ProjectPath/'Resources'
#获取当前配置文件路径
ConfigPath=ResourcesPath/'Config.ini'
#获取Qss样式路径
StylePath=str(ResourcesPath/'Style/style.qss')
#获取模型目录
ModelPath=ResourcesPath/'Model'
#获取模型音效路径
def SoundPath(modelName):
        return ModelPath/modelName/'Sound'

#获取图标路径
IconPath=ResourcesPath/'Icon'

#获取样式表
class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style=StylePath):
        with open(style, 'r',encoding="utf-8-sig") as f:
            return f.read()
        
#文件操作
class FileHandle:
    def __init__(self) :
        pass
    
    @staticmethod
    #保存到模型文件
    def saveToModel(soucePath:str,modelname:str,filename:str):
        try:
            targetDir=ModelPath/modelname
            targetDir.mkdir(parents = True, exist_ok = True)
            targetPath=targetDir/filename
            opath=QFile(soucePath)
            opath.copy(str(targetPath))
            return 1
        except:
            return 0
        
    @staticmethod
    #保存到模型的音频数据
    def saveToSound(soucePath:str,modelname:str,filename:str):
        try:
            targetDir=SoundPath(modelname)
            targetDir.mkdir(parents = True, exist_ok = True)
            targetPath=SoundPath(modelname)/filename
            opath=QFile(soucePath)
            opath.copy(str(targetPath))
            return 1
        except:
            return 0
    
    @staticmethod
    #清空文件夹内数据，如果是文件夹且为空就删除文件夹，返回1清空成功，返回0清空失败
    def LocationPath_dirDel(path):
        try:
            for path in path.iterdir():
                if path.is_dir():
                    try:
                        path.rmdir()
                    except:
                        FileHandle.LocationPath_dirDel(path)
                else:
                    path.unlink()
        except:
            path.unlink()

#重写ConfigParser的optionxform方法解决强制小写的问题
class iniParser(cp.ConfigParser):
    def __init__(self, defaults=None):
        cp.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


#配置文件操作
class ConfigHelper:
    __slots__='filename','iniFile','sections'
    def __init__(self,path=ConfigPath):
        self.filename=path
        self.iniFile=iniParser()
        self.iniFile.read(self.filename,encoding="utf-8-sig")
        self.sections=self.iniFile.sections()
    
    #文件写入操作
    def write(self):
            with open(self.filename,'w',encoding="utf-8-sig") as configfile:
                self.iniFile.write(configfile)  
        
    #添加数据
    def add(self,section,option=None,item=None):
        if section not in self.sections:
            self.iniFile.add_section(section)
        if option !=None:
            self.iniFile.set(section,option,item)
        self.write()

    #删除section
    def remove_section(self,section):
        self.iniFile.remove_section(section)
        self.write()
    #删除一个option
    def remove_option(self,section,option):
        self.iniFile.remove_option(section,option)
        self.write()
        
    #获取所有宠物
    def getPets(self):
        olist=self.iniFile.options('pets')
        del olist[0]
        return olist
    #获取宠物的数据的id（作为标记用，无实际用途）
    def getPetsId(self):
        return int(self.iniFile.get('pets','id'))
    #获取所有宠物的数据
    def getPetsItems(self):
        olist=self.iniFile.items('pets')
        del olist[0]
        return olist
    #获取所有宠物的数据
    def getPetsItemValue(self):
        reslist=[]
        olist=self.getPetsItems()
        for item in olist:
            reslist.append(literal_eval(item[1]))
        return reslist
    #添加宠物，自动设置option，id自增
    def addPets(self,petData):
        oid=self.getPetsId()+1
        option='pets'+str(oid)
        self.iniFile.set('pets','id',str(oid))
        self.iniFile.set('pets',option,petData)
        self.write()
    #删除一个宠物
    def removePets(self,option):
        self.iniFile.remove_option('pets',option)
        self.write()
    
    #获取目标宠物的所有动作
    def getActions(self,petName):
        section=petName+'_action'
        olist=self.iniFile.options(section)
        del olist[0]
        return olist
    #获取目标宠物的动作数据id
    def getActionsId(self,petName):
        section=petName+'_action'
        return int(self.iniFile.get(section,'id'))
    #获取目标宠物的所有动作数据
    def getActionsItems(self,petName):
        section=petName+'_action'
        olist=self.iniFile.items(section)
        del olist[0]
        return olist
    #获取目标宠物的所有数据值
    def getActionItemsValue(self,petName):
        reslist=[]
        olist=self.getActionsItems(petName)
        for item in olist:
            reslist.append(literal_eval(item[1]))
        return reslist
    #添加目标宠物的动作
    def addAction(self,petName,actionData):
        section=petName+'_action'
        oid=self.getActionsId(petName)+1
        option='action'+str(oid)
        self.iniFile.set(section,'id',str(oid))
        self.iniFile.set(section,option,actionData)
        self.write()
    #删除目标宠物的一个动作
    def removeAction(self,petName,option):
        section=petName+'_action'
        self.iniFile.remove_option(section,option)
    #新建一个动作数据
    def newActions(self,petName):
        section=petName+'_action'
        try:
            self.iniFile.add_section(section)
        except:
            self.iniFile.set(section,'id','0')
            self.write()
    
    #获取某个数据的源类型
    def getItemOtype(self,section,option):
        return literal_eval(self.iniFile.get(section,option))

#屏幕及窗口操作
class Screens:
    __slots__ ='desktop','screen_count','screens','primary_screen','auxiliary_screen','config','primary_width','primary_height'
    def __init__(self):
        self.config=ConfigHelper()
        self.desktop = QApplication.desktop()
        self.screen_count = self.desktop.screenCount()
        self.screens=QApplication.screens()
        self.primary_screen=self.screens[0]
        self.primary_width=self.primary_screen.availableGeometry().width()
        self.primary_height=self.primary_screen.availableGeometry().height()
        
    #获取配置文件定位信息，如果没有就在屏幕中间显示
    def GetPos(self,window):
        try:
            p=self.config.getItemOtype('systemSetting','postion')
            window.move(p.get('x'),p.get('y'))
        except:
            win_width=window.width()
            if window.height()==window.frameGeometry().height():
                win_height=window.height()
            else:
                win_height=window.frameGeometry().height()
            window.move(int((self.primary_width- win_width)/2),int((self.primary_height-win_height)/2))
        
    #获取屏幕数量
    def GetScreenCount(self):
        return self.screen_count
    #获取屏幕分辨率
    def GetScreenPixel(self,index:int=0):
        if index in range(self.screen_count):
            return self.desktop.screenGeometry(index)
        else:
            return None
    #获取屏幕可用分辨率
    def GetAvailablePixel(self,index:int=0):
        if index in range(self.screen_count):
            return self.desktop.availableGeometry(index)
        else:
            return None
    #设置屏幕固定位置
    def SetFixedPostion(self,window,pos:str):
        if window.height()==window.frameGeometry().height():
            win_height=window.height()
        else:
            win_height=window.frameGeometry().height()
        win_width=window.width()
        Dict_pos = {
        'LeftTop': {'x': 25, 'y': 25},
        'RightTop': {'x': self.primary_width - win_width-25, 'y': 25},
        'LeftBotton': {'x': 25, 'y': self.primary_height-win_height-25},
        'RightBotton': {'x': self.primary_width -win_width-25, 'y': self.primary_height-win_height-25}
        }
        p=Dict_pos.get(pos)
        window.move(p.get('x'),p.get('y'))
        self.config.add('systemSetting','postion',str(p))



if __name__=='__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow,QApplication
    #实例化窗口对象
    app = QApplication(sys.argv)
    a=Screens()
    print(a.GetAvailablePixel())
    #打开消息循环
    # sys.exit(app.exec_())