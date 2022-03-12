#!/usr/bin/env python3
# *_* coding : UTF-8 *_*

from threading import Timer
from time import sleep
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from Logic_CommonHelper import ConfigHelper

#调用B站API获取直播间信息，需要传入房间号
class IsBlive_api(QThread):
    __slots__ ='work','times','api_url','config'
    timeout = pyqtSignal(str)

    def __init__(self):
        super(IsBlive_api, self).__init__()
        self.config=ConfigHelper()
        #线程状态参数
        self.work = True
        self.times = self.config.iniFile.get('BiliBili','timeInterval')
        self.roomid=self.config.iniFile.get('BiliBili','roomid')
        if self.roomid!='':
            self.api_url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id="+self.roomid  # 刚刚获取的api
            
    def setTime(self,time):
        self.times=time
        self.config.add('BiliBili','timeInterval',time)
    
    def SetRoomId(self,roomid):
        self.api_url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id="+roomid  # 刚刚获取的api
    
    def get_api(self, item='live_status'):
        # print('进来了')
        # 开始请求
        res = requests.get(self.api_url)
        online_dic = res.json()
        if online_dic.get("message") == '房间号不存在':
            return "房间号不存在"
        else:
            try:
                online_dic = online_dic.get("data")
                return online_dic.get(item)
            except:
                return "错误:没获取到数据"
            
        
    def stop_api(self):
        self.work = False
        self.wait()
        self.exit(0)
    
    def run(self, item='live_status'):
        while self.work==True:
            self.got=self.get_api(item)
            try:
                self.timeout.emit(self.got)
            except:
                self.timeout.emit(str(self.got))
            sleep(self.times)



if __name__ == '__main__':
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    import sys
    app = QApplication(sys.argv)
    win=QWidget()
    btn=QPushButton(win)
    win.show()
    recevie = IsBlive_api()

    def Qceshi(num):
        print(num)
    
    recevie.timeout.connect(Qceshi)
    recevie.start()
    
    btn.clicked.connect(lambda:recevie.stop_api())
    
    
    sys.exit(app.exec_())


