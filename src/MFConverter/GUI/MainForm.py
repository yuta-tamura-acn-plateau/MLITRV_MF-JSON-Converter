import os
import json
import csv
import re

import xml.etree.ElementTree as ET

from itertools import islice


from PySide6.QtCore import QAbstractItemModel,QModelIndex,Qt,QItemSelectionModel
from PySide6.QtWidgets import QMainWindow,QFileDialog,QPushButton,QGridLayout,QTextEdit,QScrollArea,QTableWidgetItem,QTreeWidgetItem,QVBoxLayout,QLabel

from .MFConverterForm import Ui_MainWindow
from .ProgressDialogForm import ProgressFormClass

from converter import ConverterClass


   
#============================================================================================
class MainFormClass(QMainWindow, Ui_MainWindow):    
    converter : ConverterClass = None
    progress : ProgressFormClass = None
    path : str
    #========================================================================================
    def __init__(self, parent=None):
        super(MainFormClass, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_browse.clicked.connect(self.pushed_button)
        self.ButtonConvert.clicked.connect(self.push_convert)
        self.pushButton_ok.clicked.connect(self.push_end)
        self.ButtonConvert.setEnabled(False)
        self.ButtonConvert.setStyleSheet("background-color: white; color: grey;")
        
    #========================================================================================
    def push_next(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i+1)
    
    #========================================================================================
    def push_back(self):
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i-1)
        
    
    #========================================================================================
    def push_end(self):
        self.close()
        
    #========================================================================================
    def setProgress(self,pg):
        if self.progress == None:
            return
        self.progress.progressBar.setValue(int(pg*100))
        if pg==1:
            self.progress.set_DialogText('Finished')
            self.progress.set_ButtonText('Close')
        return 
    
    #========================================================================================
    def cancel_convert(self):
        if self.converter == None:
            return
        self.converter.exitflag = True 
        self.progress = None
        
        self.ButtonConvert.setEnabled(True)
        self.ButtonConvert.setStyleSheet("background-color: white; color: black;")
        self.pushButton_browse.setEnabled(True)
        self.pushButton_browse.setStyleSheet("background-color: white; color: black;")
        return
        
    #========================================================================================
    def dict2tree(self,obj,parent : QTreeWidgetItem ,generation : int)-> int:        
        res_g = generation
        t = type(obj)        
        if t ==dict:
            keys = list(obj.keys())
            for i in range(len(keys)):
                child = QTreeWidgetItem()
                child.setText(generation,keys[i])    
                g = self.dict2tree(obj[keys[i]],child,generation+1)
                if res_g<g:
                    res_g = g
                parent.addChild(child) 
        elif t ==list:
            for i in range(len(obj)):
                child = QTreeWidgetItem()
                child.setText(generation,str(i))
                g = self.dict2tree(obj[i],child,generation+1)
                if res_g<g:
                    res_g = g
                parent.addChild(child)
        elif t ==str:
            parent.setText(generation,obj)
        elif (t==int) or (t==float):
            parent.setText(generation,str(obj))
        else:
            parent.setText(generation,'error')
        return res_g
    
    #========================================================================================    
    def parseXML(self,element) -> QTreeWidgetItem:
        #item = QTreeWidgetItem()
        attributes = ", ".join(f"{k}={v}" for k, v in element.attrib.items())
        text = element.text.strip() if element.text else ""
        item = QTreeWidgetItem([element.tag, attributes, text])
        for child in element:
            item.addChild(self.parseXML(child))
        return item

    #========================================================================================    
    def pushed_button(self) -> str:
        if self.progress != None:
            return
        
        rootpath = os.path.abspath(os.path.dirname("__file__"))
        self.path,filter = QFileDialog.getOpenFileName(self,'openFile',rootpath,'*.json *.csv *.xml *.txt')
        self.lineEdit_path.setText(self.path)

        ext =  os.path.splitext(self.path)
        if ext[-1].casefold() == '.json'.casefold():
            self.treeWidget.takeTopLevelItem(0)
            with open(self.path,encoding="utf-8") as f:
                obj = json.load(f)
                self.stackedWidget.setCurrentIndex(3)
                json_str = json.dumps(obj)
                json_str = json_str.replace('{','\n{')
                json_str = json_str.replace('},','},\n')
                columns = 0
                if isinstance(obj, dict):
                    for key,value in obj.items():
                        rootItem = QTreeWidgetItem()
                        rootItem.setText(0,key)
                        generation = self.dict2tree(value,rootItem,1)
                        if generation > columns:
                            columns = generation
                            self.treeWidget.setColumnCount(columns+1)
                        self.treeWidget.addTopLevelItem(rootItem)
                elif isinstance(obj, list):
                    for i in range(min(len(obj),100)):
                        rootItem = QTreeWidgetItem()
                        rootItem.setText(0,str(i))
                        generation = self.dict2tree(obj[i],rootItem,1)
                        if generation > columns:
                            columns = generation
                            self.treeWidget.setColumnCount(columns+1)
                        self.treeWidget.addTopLevelItem(rootItem)
                self.textBrowser.setText(json_str)
                
        elif ext[-1].casefold() =='.csv'.casefold():
            obj = list()
            with open(self.path,encoding="shift-jis") as f:#ERROR CHECK ENCORDING
                for line in islice(f, 21):
                    obj.append(re.split(',|\n',line))
                    
                self.stackedWidget.setCurrentIndex(1)
                self.tableWidget.setRowCount(len(obj)-1)
                self.tableWidget.setColumnCount(len(obj[0])-1)                     
                t = ''
                for i in range(0, len(obj)-1):                    
                    for j in range(0,len(obj[i])-1):
                        self.tableWidget.setItem(i,j,QTableWidgetItem(obj[i][j]))                        
                        t = t+obj[i][j]+','
                    t =t+'\n'
                self.textBrowser.setText(t)                  
                
        elif ext[-1].casefold() =='.xml'.casefold():
            self.treeWidget.takeTopLevelItem(0)
            tree = ET.parse(self.path)    
            root = tree.getroot()
            self.stackedWidget.setCurrentIndex(3)
            self.treeWidget.setColumnCount(4)            
            rootItem = self.parseXML(root)
            self.treeWidget.addTopLevelItem(rootItem)     
        else:
            pass
        
        if len(self.path)>0:
            self.ButtonConvert.setEnabled(True)
            self.ButtonConvert.setStyleSheet("background-color: white; color: black;")
        else:
            self.ButtonConvert.setEnabled(False)    
            self.ButtonConvert.setStyleSheet("background-color: white; color: grey;")
            
        return self.path
    
    #========================================================================================
    def push_convert(self):
        self.ButtonConvert.setEnabled(False)
        self.ButtonConvert.setStyleSheet("background-color: white; color: grey;")
        self.pushButton_browse.setEnabled(False)
        self.pushButton_browse.setStyleSheet("background-color: white; color: grey;")
        
        self.converter = ConverterClass()
        self.converter.set_path(self.path)
                
        self.progress =ProgressFormClass()
        self.progress.cancelButton.clicked.connect(self.cancel_convert)
        self.progress.show()
        self.converter.progress_callback = self.setProgress
                                
        self.converter.start()
        pass
    
    
#mainFormClass