# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wid_calibra.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_widCal(object):
    def setupUi(self, widCal):
        widCal.setObjectName(_fromUtf8("widCal"))
        widCal.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(widCal)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gbx_sonar = QtGui.QGroupBox(widCal)
        self.gbx_sonar.setObjectName(_fromUtf8("gbx_sonar"))
        self.horizontalLayout.addWidget(self.gbx_sonar)

        self.retranslateUi(widCal)
        QtCore.QMetaObject.connectSlotsByName(widCal)

    def retranslateUi(self, widCal):
        widCal.setWindowTitle(_translate("widCal", "Calibrate", None))
        self.gbx_sonar.setTitle(_translate("widCal", "Sonar", None))

