import sys

from PySide6.QtWidgets import  QApplication
from concurrent.futures import ThreadPoolExecutor

from GUI.MainForm import MainFormClass
#from converter import ConverterClass

                         
#============================================================================================
def main():
    qAp = QApplication(sys.argv)
    main_gui = MainFormClass()
    main_gui.show()
    qAp.exec()
            
    return

#============================================================================================
if __name__=="__main__":
    main()