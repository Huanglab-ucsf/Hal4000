# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sharpnessdetector.ui'
#
# Created: Fri Feb 27 18:40:38 2015
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(561, 640)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(561, 640))
        Dialog.setMaximumSize(QtCore.QSize(561, 640))
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HAL-4000 Sharpness Detector", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(480, 610, 75, 24))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 541, 591))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.countsTab = QtGui.QWidget()
        self.countsTab.setObjectName(_fromUtf8("countsTab"))
        self.graphFrame = QtGui.QFrame(self.countsTab)
        self.graphFrame.setGeometry(QtCore.QRect(60, 40, 471, 371))
        self.graphFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.graphFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.graphFrame.setObjectName(_fromUtf8("graphFrame"))
        self.countsText1 = QtGui.QLabel(self.countsTab)
        self.countsText1.setGeometry(QtCore.QRect(20, 10, 171, 16))
        self.countsText1.setText(QtGui.QApplication.translate("Dialog", "Sharpness running average:", None, QtGui.QApplication.UnicodeUTF8))
        self.countsText1.setObjectName(_fromUtf8("countsText1"))
        self.countsLabel1 = QtGui.QLabel(self.countsTab)
        self.countsLabel1.setGeometry(QtCore.QRect(170, 10, 121, 20))
        self.countsLabel1.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.countsLabel1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.countsLabel1.setObjectName(_fromUtf8("countsLabel1"))
        self.label = QtGui.QLabel(self.countsTab)
        self.label.setGeometry(QtCore.QRect(100, 520, 341, 20))
        self.label.setText(QtGui.QApplication.translate("Dialog", "This Space Intentionally Left Blank", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.minSpinBox = QtGui.QSpinBox(self.countsTab)
        self.minSpinBox.setGeometry(QtCore.QRect(5, 400, 51, 22))
        self.minSpinBox.setMaximum(1000)
        self.minSpinBox.setSingleStep(1)
        self.minSpinBox.setObjectName(_fromUtf8("minSpinBox"))
        self.maxSpinBox = QtGui.QSpinBox(self.countsTab)
        self.maxSpinBox.setGeometry(QtCore.QRect(5, 30, 51, 22))
        self.maxSpinBox.setMinimum(2)
        self.maxSpinBox.setMaximum(1000)
        self.maxSpinBox.setSingleStep(1)
        self.maxSpinBox.setProperty("value", 5)
        self.maxSpinBox.setObjectName(_fromUtf8("maxSpinBox"))
        self.countsLabel2 = QtGui.QLabel(self.countsTab)
        self.countsLabel2.setGeometry(QtCore.QRect(390, 430, 121, 20))
        self.countsLabel2.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.countsLabel2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.countsLabel2.setObjectName(_fromUtf8("countsLabel2"))
        self.label_2 = QtGui.QLabel(self.countsTab)
        self.label_2.setGeometry(QtCore.QRect(30, 450, 81, 16))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Scale factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.scale_lineEdit = QtGui.QLineEdit(self.countsTab)
        self.scale_lineEdit.setGeometry(QtCore.QRect(100, 450, 113, 20))
        self.scale_lineEdit.setObjectName(_fromUtf8("scale_lineEdit"))
        self.tabWidget.addTab(self.countsTab, _fromUtf8(""))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.countsTab), QtGui.QApplication.translate("Dialog", "Sharpness", None, QtGui.QApplication.UnicodeUTF8))

