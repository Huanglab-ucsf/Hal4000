# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mosaic.ui'
#
# Created: Wed Aug 20 14:53:24 2014
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
        Dialog.resize(510, 310)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(510, 310))
        Dialog.setMaximumSize(QtCore.QSize(510, 310))
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HAL-4000 Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicBox = QtGui.QGroupBox(Dialog)
        self.mosaicBox.setGeometry(QtCore.QRect(10, 0, 491, 271))
        self.mosaicBox.setTitle(QtGui.QApplication.translate("Dialog", "Mosaic", None, QtGui.QApplication.UnicodeUTF8))
        self.mosaicBox.setObjectName(_fromUtf8("mosaicBox"))
        self.modeBox = QtGui.QGroupBox(self.mosaicBox)
        self.modeBox.setGeometry(QtCore.QRect(10, 20, 181, 151))
        self.modeBox.setTitle(QtGui.QApplication.translate("Dialog", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.modeBox.setObjectName(_fromUtf8("modeBox"))
        self.modeWidget = QtGui.QWidget(self.modeBox)
        self.modeWidget.setGeometry(QtCore.QRect(7, 12, 101, 131))
        self.modeWidget.setObjectName(_fromUtf8("modeWidget"))
        self.mosaicDisplayWidget = QtGui.QWidget(self.mosaicBox)
        self.mosaicDisplayWidget.setGeometry(QtCore.QRect(193, 20, 298, 249))
        self.mosaicDisplayWidget.setObjectName(_fromUtf8("mosaicDisplayWidget"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(430, 280, 75, 24))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setObjectName(_fromUtf8("okButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

