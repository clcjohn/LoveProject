import sys
from PyQt5.QtWidgets import QApplication
from Logic_PetFrom import *
from Logic_Tray import *
from UI_SetFrom import *
from Logic_CommonHelper import CommonHelper




if __name__=='__main__':
    app=QApplication(sys.argv)
    qssStyle = CommonHelper.readQss()
    win=Pet()
    mtray=tray(win)
    sc=Screens()
    sc.GetPos(win)
    sf=SetFrom(win)
    sf(mtray.SetFromShow)
    sf(win.rightMenu.SetFromShow)
    win.setStyleSheet(qssStyle)
    win.show()
    sys.exit(app.exec())