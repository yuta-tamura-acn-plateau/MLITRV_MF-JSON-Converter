# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MFConverterForm.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(725, 451)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_hint = QVBoxLayout()
        self.verticalLayout_hint.setObjectName(u"verticalLayout_hint")

        self.verticalLayout.addLayout(self.verticalLayout_hint)

        self.horizontalLayout_path = QHBoxLayout()
        self.horizontalLayout_path.setObjectName(u"horizontalLayout_path")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(75, 24))

        self.horizontalLayout_path.addWidget(self.label)

        self.lineEdit_path = QLineEdit(self.centralwidget)
        self.lineEdit_path.setObjectName(u"lineEdit_path")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_path.setSizePolicy(sizePolicy3)
        self.lineEdit_path.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_path.addWidget(self.lineEdit_path)

        self.pushButton_browse = QPushButton(self.centralwidget)
        self.pushButton_browse.setObjectName(u"pushButton_browse")
        sizePolicy2.setHeightForWidth(self.pushButton_browse.sizePolicy().hasHeightForWidth())
        self.pushButton_browse.setSizePolicy(sizePolicy2)

        self.horizontalLayout_path.addWidget(self.pushButton_browse)


        self.verticalLayout.addLayout(self.horizontalLayout_path)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.ButtonConvert = QPushButton(self.centralwidget)
        self.ButtonConvert.setObjectName(u"ButtonConvert")

        self.horizontalLayout.addWidget(self.ButtonConvert)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_main = QVBoxLayout()
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_tree = QWidget()
        self.page_tree.setObjectName(u"page_tree")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.page_tree.sizePolicy().hasHeightForWidth())
        self.page_tree.setSizePolicy(sizePolicy4)
        self.page_tree.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.page_tree)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.treeWidget = QTreeWidget(self.page_tree)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_4.addWidget(self.treeWidget)

        self.stackedWidget.addWidget(self.page_tree)
        self.page_table = QWidget()
        self.page_table.setObjectName(u"page_table")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.page_table.sizePolicy().hasHeightForWidth())
        self.page_table.setSizePolicy(sizePolicy5)
        self.page_table.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.page_table)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableWidget = QTableWidget(self.page_table)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy6)

        self.verticalLayout_5.addWidget(self.tableWidget)

        self.stackedWidget.addWidget(self.page_table)
        self.page_texts = QWidget()
        self.page_texts.setObjectName(u"page_texts")
        self.page_texts.setMinimumSize(QSize(703, 0))
        self.verticalLayout_6 = QVBoxLayout(self.page_texts)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.textBrowser = QTextBrowser(self.page_texts)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_6.addWidget(self.textBrowser)

        self.stackedWidget.addWidget(self.page_texts)

        self.verticalLayout_main.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.verticalLayout_main)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.centralwidget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        sizePolicy2.setHeightForWidth(self.pushButton_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_ok.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.pushButton_ok)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MFConverter", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5909\u63db\u30d5\u30a1\u30a4\u30eb", None))
        self.pushButton_browse.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u7167", None))
        self.ButtonConvert.setText(QCoreApplication.translate("MainWindow", u"\u5909\u63db", None))
        self.pushButton_ok.setText(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
    # retranslateUi

