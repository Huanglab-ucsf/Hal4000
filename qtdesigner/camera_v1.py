# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera-v1.ui'
#
# Created: Mon Mar 10 11:10:40 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(636, 581)
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.scaleMin = QtGui.QLabel(Frame)
        self.scaleMin.setGeometry(QtCore.QRect(540, 510, 46, 14))
        self.scaleMin.setText(QtGui.QApplication.translate("Frame", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleMin.setAlignment(QtCore.Qt.AlignCenter)
        self.scaleMin.setObjectName(_fromUtf8("scaleMin"))
        self.cameraDisplayFrame = QtGui.QFrame(Frame)
        self.cameraDisplayFrame.setGeometry(QtCore.QRect(0, 0, 532, 532))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraDisplayFrame.sizePolicy().hasHeightForWidth())
        self.cameraDisplayFrame.setSizePolicy(sizePolicy)
        self.cameraDisplayFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.cameraDisplayFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.cameraDisplayFrame.setObjectName(_fromUtf8("cameraDisplayFrame"))
        self.autoScaleButton = QtGui.QPushButton(Frame)
        self.autoScaleButton.setGeometry(QtCore.QRect(450, 540, 75, 24))
        self.autoScaleButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.autoScaleButton.setText(QtGui.QApplication.translate("Frame", "Autoscale", None, QtGui.QApplication.UnicodeUTF8))
        self.autoScaleButton.setObjectName(_fromUtf8("autoScaleButton"))
        self.intensityIntLabel = QtGui.QLabel(Frame)
        self.intensityIntLabel.setGeometry(QtCore.QRect(290, 545, 41, 16))
        self.intensityIntLabel.setText(QtGui.QApplication.translate("Frame", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.intensityIntLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.intensityIntLabel.setObjectName(_fromUtf8("intensityIntLabel"))
        self.syncSpinBox = QtGui.QSpinBox(Frame)
        self.syncSpinBox.setGeometry(QtCore.QRect(384, 542, 46, 22))
        self.syncSpinBox.setObjectName(_fromUtf8("syncSpinBox"))
        self.scaleMax = QtGui.QLabel(Frame)
        self.scaleMax.setGeometry(QtCore.QRect(540, 11, 46, 14))
        self.scaleMax.setText(QtGui.QApplication.translate("Frame", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleMax.setAlignment(QtCore.Qt.AlignCenter)
        self.scaleMax.setObjectName(_fromUtf8("scaleMax"))
        self.syncLabel = QtGui.QLabel(Frame)
        self.syncLabel.setGeometry(QtCore.QRect(344, 545, 41, 16))
        self.syncLabel.setText(QtGui.QApplication.translate("Frame", "Display:", None, QtGui.QApplication.UnicodeUTF8))
        self.syncLabel.setObjectName(_fromUtf8("syncLabel"))
        self.colorFrame = QtGui.QFrame(Frame)
        self.colorFrame.setGeometry(QtCore.QRect(580, 30, 20, 471))
        self.colorFrame.setFrameShape(QtGui.QFrame.Panel)
        self.colorFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.colorFrame.setObjectName(_fromUtf8("colorFrame"))
        self.colorComboBox = QtGui.QComboBox(Frame)
        self.colorComboBox.setGeometry(QtCore.QRect(530, 540, 74, 22))
        self.colorComboBox.setObjectName(_fromUtf8("colorComboBox"))
        self.intensityPosLabel = QtGui.QLabel(Frame)
        self.intensityPosLabel.setGeometry(QtCore.QRect(250, 543, 61, 20))
        self.intensityPosLabel.setText(QtGui.QApplication.translate("Frame", "(0,0)", None, QtGui.QApplication.UnicodeUTF8))
        self.intensityPosLabel.setObjectName(_fromUtf8("intensityPosLabel"))

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        pass

