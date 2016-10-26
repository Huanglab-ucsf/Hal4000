# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pf.ui'
#
# Created: Wed Jan 28 13:18:17 2015
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
        Dialog.resize(526, 560)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(510, 310))
        Dialog.setMaximumSize(QtCore.QSize(800, 800))
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HAL-4000 Pupil Function Retrieval", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicBox = QtGui.QGroupBox(Dialog)
        self.mosaicBox.setGeometry(QtCore.QRect(10, 0, 471, 481))
        self.mosaicBox.setTitle(QtGui.QApplication.translate("Dialog", "Pupil Function Retrieval", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicBox.setObjectName(_fromUtf8("mosaicBox"))
        self.modeBox = QtGui.QGroupBox(self.mosaicBox)
        self.modeBox.setGeometry(QtCore.QRect(10, 20, 181, 291))
        self.modeBox.setTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.modeBox.setObjectName(_fromUtf8("modeBox"))
        self.label = QtGui.QLabel(self.modeBox)
        self.label.setGeometry(QtCore.QRect(10, 80, 81, 16))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Step size (nm):", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.stepSize_lineEdit = QtGui.QLineEdit(self.modeBox)
        self.stepSize_lineEdit.setGeometry(QtCore.QRect(90, 80, 71, 20))
        self.stepSize_lineEdit.setObjectName(_fromUtf8("stepSize_lineEdit"))
        self.label_2 = QtGui.QLabel(self.modeBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 71, 16))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "First frame:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.startFrame_lineEdit = QtGui.QLineEdit(self.modeBox)
        self.startFrame_lineEdit.setGeometry(QtCore.QRect(90, 110, 71, 20))
        self.startFrame_lineEdit.setObjectName(_fromUtf8("startFrame_lineEdit"))
        self.label_3 = QtGui.QLabel(self.modeBox)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 71, 16))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Last frame:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.stopFrame_lineEdit = QtGui.QLineEdit(self.modeBox)
        self.stopFrame_lineEdit.setGeometry(QtCore.QRect(90, 140, 71, 20))
        self.stopFrame_lineEdit.setObjectName(_fromUtf8("stopFrame_lineEdit"))
        self.label_4 = QtGui.QLabel(self.modeBox)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 46, 13))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Center x:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.centerX_lineEdit = QtGui.QLineEdit(self.modeBox)
        self.centerX_lineEdit.setGeometry(QtCore.QRect(90, 170, 71, 20))
        self.centerX_lineEdit.setObjectName(_fromUtf8("centerX_lineEdit"))
        self.label_5 = QtGui.QLabel(self.modeBox)
        self.label_5.setGeometry(QtCore.QRect(10, 200, 46, 13))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Center y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.centerY_lineEdit = QtGui.QLineEdit(self.modeBox)
        self.centerY_lineEdit.setGeometry(QtCore.QRect(90, 200, 71, 20))
        self.centerY_lineEdit.setObjectName(_fromUtf8("centerY_lineEdit"))
        self.setParams_pushButton = QtGui.QPushButton(self.modeBox)
        self.setParams_pushButton.setGeometry(QtCore.QRect(90, 230, 75, 23))
        self.setParams_pushButton.setText(QtGui.QApplication.translate("Dialog", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.setParams_pushButton.setObjectName(_fromUtf8("setParams_pushButton"))
        self.findPF_pushButton = QtGui.QPushButton(self.modeBox)
        self.findPF_pushButton.setGeometry(QtCore.QRect(90, 260, 75, 23))
        self.findPF_pushButton.setText(QtGui.QApplication.translate("Dialog", "Find PF", None, QtGui.QApplication.UnicodeUTF8))
        self.findPF_pushButton.setObjectName(_fromUtf8("findPF_pushButton"))
        self.recordPSF_checkBox = QtGui.QCheckBox(self.modeBox)
        self.recordPSF_checkBox.setGeometry(QtCore.QRect(20, 30, 131, 17))
        self.recordPSF_checkBox.setText(QtGui.QApplication.translate("Dialog", "Record PSF", None, QtGui.QApplication.UnicodeUTF8))
        self.recordPSF_checkBox.setObjectName(_fromUtf8("recordPSF_checkBox"))
        self.labelDisplay = QtGui.QLabel(self.mosaicBox)
        self.labelDisplay.setGeometry(QtCore.QRect(200, 20, 256, 256))
        self.labelDisplay.setFrameShape(QtGui.QFrame.Box)
        self.labelDisplay.setText(_fromUtf8(""))
        self.labelDisplay.setObjectName(_fromUtf8("labelDisplay"))
        self.labelDisplay_2 = QtGui.QLabel(self.mosaicBox)
        self.labelDisplay_2.setGeometry(QtCore.QRect(200, 280, 256, 100))
        self.labelDisplay_2.setFrameShape(QtGui.QFrame.Box)
        self.labelDisplay_2.setText(_fromUtf8(""))
        self.labelDisplay_2.setObjectName(_fromUtf8("labelDisplay_2"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(410, 500, 75, 24))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setObjectName(_fromUtf8("okButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

