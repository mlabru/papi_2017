#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_calibra

a serial port packet monitor that plots live data using PyQwt

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# view
import view.wid_calibra_ui as wcui

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetCalibra >-------------------------------------------------------------------------------

class CWidgetCalibra(QtGui.QWidget, wcui.Ui_widCal):
    """
    a serial port packet monitor that plots live data using PyQwt
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent):
        """
        constructor
        """
        # init super class
        super(CWidgetCalibra, self).__init__(f_parent)

        self.__v_documentIsDirty = False

        self.__config = None  # Configuration(self)
        # assert self.__config 

        self.__v_portValid = False

        self.setupUi(self)

        #self.__load_document(settings.value("Last Configuration").toString())
    '''
    # ---------------------------------------------------------------------------------------------
    # QEvent
    def changeEvent(self, e):

        super(CWidgetCalibra, self).changeEvent(e)

        if QtCore.QEvent.LanguageChange == e.type():
            self.retranslateUi(self)

    # ---------------------------------------------------------------------------------------------
    def checkDocument(self):

        if self.__v_documentIsDirty:
            if QMessageBox.No == QMessageBox.warning(0, "", "Current configuration was changed but not saved.\nAre you sure you want to proceed ?", QMessageBox.Yes, QMessageBox.No | QMessageBox.Default):
                return False

        return True

    # ---------------------------------------------------------------------------------------------
    # QCloseEvent
    def closeEvent(self, e):

        if self.__v_portValid:
            port.requestToStop()

        if not checkDocument():
            e.ignore()

    # ---------------------------------------------------------------------------------------------
    # const QString&
    def __load_document(self, filePath):

        success = True
        file = QFile(filePath)

        if file.open(QIODevice.ReadOnly):

            textStream = QTextStream(file)
            self.configurationText.setPlainText(textStream.readAll())
            updateDocumentFilePath(filePath)
            success = True


        if not success:
            QMessageBox.critical(0, "", "Could not load file: " + filePath)

        return success

    # ---------------------------------------------------------------------------------------------
    # const QString&, const QString&
    def message(self, text, type):

        if "critical" == type:
            QMessageBox.critical(0, "", text)

        else:
            QMessageBox.information(0, "", text)

    # ---------------------------------------------------------------------------------------------
    def portStopped(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)
        self.actionRun.setEnabled(True)

        port.deleteLater()

        self.__v_portValid = False

    # ---------------------------------------------------------------------------------------------
    # const QString&
    def saveDocument(self, filePath):

        success = False
        file = QFile(filePath)

        if file.open(QIODevice.WriteOnly):

            textStream = QTextStream(file)
            textStream << self.configurationText.toPlainText()
            textStream.flush()

            self.__v_documentIsDirty  = False

            updateDocumentFilePath(filePath)

            success = True

        if not success:
            QMessageBox.critical(0, "", "Could not save file: " + filePath)

        else:
            self.statusBar.showMessage("File Saved", 2000)

        return success

    # ---------------------------------------------------------------------------------------------
    # const QString&
    def updateDocumentFilePath(self, filePath):

        documentFilePath = filePath

        settings.setValue("Last Configuration", filePath)

        self.setWindowTitle("TTY Monitor - " + QFileInfo(filePath).fileName())

        self.__v_documentIsDirty  = False

    # =============================================================================================
    # callbacks
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    def on_actionAbout_triggered(self):

        QMessageBox.about(0, "XXX", "YYY")

    # ---------------------------------------------------------------------------------------------
    def on_actionChart_toggled(self, b):

        self.dockWidgetChart.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_actionConfiguration_toggled(self, b):

        self.dockWidgetConfiguration.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_actionExit_triggered(self):

        self.close()

    # ---------------------------------------------------------------------------------------------
    def on_actionNew_triggered(self):

        if checkDocument():

            self.configurationText.clear()
            documentFilePath = ""
            self.statusBar.showMessage(documentFilePath)
            self.__v_documentIsDirty  = False

    # ---------------------------------------------------------------------------------------------
    def on_actionOpen_triggered(self):

        if not checkDocument():
            return

        filePath = QFileDialog.getOpenFileName(self, tr("Open File"), 
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.__load_document(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionRun_triggered(self):

        self.__config.parse( self.configurationText.toPlainText())
        self.dataText.setMaximumBlockCount(MAX(1, self.__config.get("_setup_", "width").toInt()))

        self.chart.init(self.__config)
        self.actionRun.setEnabled(False)
        self.actionStop.setEnabled(True)
        self.sendButton.setEnabled(True)
        self.dataText.clear()

        port = createPort(self.__config)

        decoder = createDecoder(self, self.__config)
        display = createDisplay(self, self.__config)

        self.__v_portValid = True

        # port signals
        #connect(port,SIGNAL(newData(const QByteArray&)),decoder,SLOT(newData(const QByteArray&)))
        #connect(port,SIGNAL(packetSeparator()),decoder,SLOT(packetSeparator()))
        #connect(port,SIGNAL(stopped()),self,SLOT(portStopped()))
        #connect(port,SIGNAL(message(const QString&,const QString&)),self,SLOT(message(const QString&,const QString&)))

        # decoder signals
        #connect(decoder,SIGNAL(newPacket(DecoderBase*)),self.chart,SLOT(newPacket(DecoderBase*)))
        #connect(decoder,SIGNAL(newPacket(DecoderBase*)),display,SLOT(newPacket(DecoderBase*)))

        # display signals
        #connect(display,SIGNAL(newDisplay(const QString&)),self.dataText,SLOT(appendPlainText(const QString&)))

        port.start()

    # ---------------------------------------------------------------------------------------------
    def on_actionSave_triggered(self):

        if documentFilePath.isEmpty():
            on_actionSaveAs_triggered()

        else:
            saveDocument(documentFilePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionSaveAs_triggered(self):

        filePath = QFileDialog.getSaveFileName(self, tr("Save File"),
                       documentFilePath, tr("TTY Monitor Configuration (*.scc)All Files (*.*)"))

        if not filePath.isEmpty():
            self.saveDocument(filePath)

    # ---------------------------------------------------------------------------------------------
    def on_actionStop_triggered(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)

        port.requestToStop()

    # ---------------------------------------------------------------------------------------------
    def on_actionToolbar_toggled(self, b):

        self.mainToolBar.setVisible(b)

    # ---------------------------------------------------------------------------------------------
    def on_configurationText_textChanged(self):

        self.__v_documentIsDirty = True

    # ---------------------------------------------------------------------------------------------
    def on_sendButton_clicked(self):

        if self.__v_portValid:
            port.send(self.sendText.text())
    '''
# < the end >--------------------------------------------------------------------------------------
        