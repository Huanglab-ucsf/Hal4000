# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera-params-v1.ui'
#
# Created: Mon Mar 10 11:11:54 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName(_fromUtf8("GroupBox"))
        GroupBox.resize(231, 151)
        GroupBox.setWindowTitle(QtGui.QApplication.translate("GroupBox", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        GroupBox.setTitle(QtGui.QApplication.translate("GroupBox", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.exposureTimeText = QtGui.QLabel(GroupBox)
        self.exposureTimeText.setGeometry(QtCore.QRect(120, 80, 101, 16))
        self.exposureTimeText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.exposureTimeText.setText(_fromUtf8(""))
        self.exposureTimeText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.exposureTimeText.setObjectName(_fromUtf8("exposureTimeText"))
        self.exposureTimeLabel = QtGui.QLabel(GroupBox)
        self.exposureTimeLabel.setGeometry(QtCore.QRect(10, 80, 101, 16))
        self.exposureTimeLabel.setText(QtGui.QApplication.translate("GroupBox", "Exposure Time (s):", None, QtGui.QApplication.UnicodeUTF8))
        self.exposureTimeLabel.setObjectName(_fromUtf8("exposureTimeLabel"))
        self.EMCCDLabel = QtGui.QLabel(GroupBox)
        self.EMCCDLabel.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.EMCCDLabel.setText(QtGui.QApplication.translate("GroupBox", "EMCCD Gain: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.EMCCDLabel.setObjectName(_fromUtf8("EMCCDLabel"))
        self.preampGainLabel = QtGui.QLabel(GroupBox)
        self.preampGainLabel.setGeometry(QtCore.QRect(11, 40, 101, 16))
        self.preampGainLabel.setText(QtGui.QApplication.translate("GroupBox", "Preamp Gain:", None, QtGui.QApplication.UnicodeUTF8))
        self.preampGainLabel.setObjectName(_fromUtf8("preampGainLabel"))
        self.temperatureLabel = QtGui.QLabel(GroupBox)
        self.temperatureLabel.setGeometry(QtCore.QRect(10, 120, 111, 16))
        self.temperatureLabel.setText(QtGui.QApplication.translate("GroupBox", "Temperature (C):", None, QtGui.QApplication.UnicodeUTF8))
        self.temperatureLabel.setObjectName(_fromUtf8("temperatureLabel"))
        self.pictureSizeText = QtGui.QLabel(GroupBox)
        self.pictureSizeText.setGeometry(QtCore.QRect(120, 60, 101, 16))
        self.pictureSizeText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pictureSizeText.setText(_fromUtf8(""))
        self.pictureSizeText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pictureSizeText.setObjectName(_fromUtf8("pictureSizeText"))
        self.FPSLabel = QtGui.QLabel(GroupBox)
        self.FPSLabel.setGeometry(QtCore.QRect(10, 100, 101, 16))
        self.FPSLabel.setText(QtGui.QApplication.translate("GroupBox", "FPS (Hz):", None, QtGui.QApplication.UnicodeUTF8))
        self.FPSLabel.setObjectName(_fromUtf8("FPSLabel"))
        self.preampGainText = QtGui.QLabel(GroupBox)
        self.preampGainText.setGeometry(QtCore.QRect(121, 40, 101, 16))
        self.preampGainText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.preampGainText.setText(_fromUtf8(""))
        self.preampGainText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.preampGainText.setObjectName(_fromUtf8("preampGainText"))
        self.temperatureText = QtGui.QLabel(GroupBox)
        self.temperatureText.setGeometry(QtCore.QRect(120, 120, 101, 16))
        self.temperatureText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.temperatureText.setText(_fromUtf8(""))
        self.temperatureText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.temperatureText.setObjectName(_fromUtf8("temperatureText"))
        self.EMCCDSlider = QtGui.QSlider(GroupBox)
        self.EMCCDSlider.setGeometry(QtCore.QRect(118, 19, 101, 20))
        self.EMCCDSlider.setMaximum(100)
        self.EMCCDSlider.setProperty("value", 0)
        self.EMCCDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.EMCCDSlider.setObjectName(_fromUtf8("EMCCDSlider"))
        self.FPSText = QtGui.QLabel(GroupBox)
        self.FPSText.setGeometry(QtCore.QRect(120, 100, 101, 16))
        self.FPSText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.FPSText.setText(_fromUtf8(""))
        self.FPSText.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FPSText.setObjectName(_fromUtf8("FPSText"))
        self.pictureSizeLabel = QtGui.QLabel(GroupBox)
        self.pictureSizeLabel.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.pictureSizeLabel.setText(QtGui.QApplication.translate("GroupBox", "Picture Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.pictureSizeLabel.setObjectName(_fromUtf8("pictureSizeLabel"))

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        pass

