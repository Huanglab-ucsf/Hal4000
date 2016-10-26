# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'illumination-v1.ui'
#
# Created: Mon Mar 10 11:16:14 2014
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
        Dialog.resize(372, 312)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(372, 312))
        Dialog.setMaximumSize(QtCore.QSize(372, 312))
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HAL-4000 Illumination", None, QtGui.QApplication.UnicodeUTF8))
        self.laserBox = QtGui.QGroupBox(Dialog)
        self.laserBox.setGeometry(QtCore.QRect(10, 0, 354, 271))
        self.laserBox.setTitle(QtGui.QApplication.translate("Dialog", "Laser Power Control", None, QtGui.QApplication.UnicodeUTF8))
        self.laserBox.setObjectName(_fromUtf8("laserBox"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(290, 280, 75, 24))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setObjectName(_fromUtf8("okButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

