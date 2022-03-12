#!/usr/bin/env python3
# *_* coding : UTF-8 *_*
from Logic_CommonHelper import Path,ModelPath,SoundPath,ResourcesPath
from PyQt5.QtCore import QFile

class FileHandle:
    def __init__(self) :
        pass
    
    @staticmethod
    #保存到模型文件
    def saveToModel(soucePath:str,modelname:str,filename:str):
        targetDir=ModelPath/modelname
        targetDir.mkdir(parents = True, exist_ok = True)
        targetPath=targetDir/filename
        opath=QFile(soucePath)
        opath.copy(str(targetPath))
        
    @staticmethod
    #保存到模型的音频数据
    def saveToSound(soucePath:str,modelname:str,filename:str):
        targetDir=SoundPath(modelname)
        targetDir.mkdir(parents = True, exist_ok = True)
        targetPath=SoundPath(modelname)/filename
        opath=QFile(soucePath)
        opath.copy(str(targetPath))



if __name__=='__main__':
    pass
