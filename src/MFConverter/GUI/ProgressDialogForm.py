from re import S
import time
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget

from .UiProgressDialog import Ui_ProgressDialogClass

#============================================================================================
class ProgressFormClass(QWidget, Ui_ProgressDialogClass):
    #========================================================================================
    def __init__(self, parent=None):
        super(ProgressFormClass ,self).__init__(parent)
        self.setupUi(self)
        
    #========================================================================================
    def set_ButtonText(self,txt):
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", txt, None))
        
    #========================================================================================
    def set_DialogText(self,txt):
        self.labelDialogMain.setText(QCoreApplication.translate("MainWindow", txt, None))

   