#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_net_monitor

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

# model
import model.pc_syntax as sntx
import model.pc_altimeter_feed as altf
import model.pc_camera_feed as camf

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetNetMonitor >----------------------------------------------------------------------------

class CWidgetNetMonitor(QtGui.QWidget):
    """
    network packet monitor that plots live data using PyQwt
    """
    # signal
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)
    C_SGN_NEW_MSG_SNS = QtCore.pyqtSignal(str)
    C_SGN_NEW_MSG_CAM = QtCore.pyqtSignal(str)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_settings, f_parent=None):
        """
        constructor
        """
        # init super class
        super(CWidgetNetMonitor, self).__init__(f_parent)

        # save settings
        self.__settings = f_settings

        # parent
        self.__parent = f_parent

        # config file path  
        self.__s_config_file_path = None

        # flag dirty
        self.__v_config_file_is_dirty = False

        # config
        self.__config = None  # Configuration(self)
        # assert self.__config

        # create camera groupBox
        lgbx_cam = self.__create_gbx_cam()

        # create CCC groupBox
        lgbx_ccc = self.__create_gbx_ccc()

        # create sensors groupBox
        lgbx_sns = self.__create_gbx_sns()

        # create configuration groupBox
        self.__gbx_cnf = self.__create_gbx_config()

        # create net monitor toolbar
        self.__tbr_nmon = self.__create_toolbar(f_parent)

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes on a grid
        llo_grid.addWidget(self.__gbx_cnf, 0, 0, 1, 1)
        llo_grid.addWidget(lgbx_cam,       0, 1, 1, 1)
        llo_grid.addWidget(lgbx_ccc,       1, 0, 1, 1)
        llo_grid.addWidget(lgbx_sns,       1, 1, 1, 1)

        # make connections
        self.C_SGN_PAGE_ON.connect(self.__on_page_on)
        self.C_SGN_NEW_MSG_SNS.connect(self.__on_msg_sensor)
        self.C_SGN_NEW_MSG_CAM.connect(self.__on_msg_camera)

        # load config file
        self.__load_config_file()
    '''
    # ---------------------------------------------------------------------------------------------
    # QEvent
    def changeEvent(self, e):

        super(CWidgetNetMonitor, self).changeEvent(e)

        if QtCore.QEvent.LanguageChange == e.type():
            self.retranslateUi(self)
    '''
    # ---------------------------------------------------------------------------------------------
    def __check_config_file(self):
        """
        check config_file
        """
        # dirty ?
        if self.__v_config_file_is_dirty:
            # save ?
            if QtGui.QMessageBox.No == QtGui.QMessageBox.warning(self, "",
                "Current configuration was changed but not saved.\nAre you sure you want to proceed ?",
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No | QtGui.QMessageBox.Default):
                # return
                return False

        # return
        return True

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtGui.QCloseEvent)
    def closeEvent(self, f_evt):
        """
        close event callback
        """
        # don't save config file ?
        if not __check_config_file():
            # ignore
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_cam(self):
        """
        create camera groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setFamily("Courier")
        l_font.setPointSize(12)

        # create QPlainTextEdit camera
        self.__pte_camera = QtGui.QPlainTextEdit()
        assert self.__pte_camera

        # setup
        self.__pte_camera.setFont(l_font)
        self.__pte_camera.setReadOnly(True)
        self.__pte_camera.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_camera.setMinimumSize(QtCore.QSize(500, 270))
        self.__pte_camera.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put camera on layout
        llay_gbx.addWidget(self.__pte_camera)

        # create groupBox camera
        lgbx_cam = QtGui.QGroupBox(u"Camera", self)
        assert lgbx_cam

        # setup
        lgbx_cam.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        lgbx_cam.setLayout(llay_gbx)

        # return
        return lgbx_cam

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_ccc(self):
        """
        create CCC groupBox
        """
        # create altimeter widget
        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setFamily("Courier")
        l_font.setPointSize(12)

        # create QPlainTextEdit CCC
        self.__pte_ccc = QtGui.QPlainTextEdit()
        assert self.__pte_ccc

        self.__pte_ccc.setFont(l_font)
        self.__pte_ccc.setReadOnly(True)
        self.__pte_ccc.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_ccc.setMinimumSize(QtCore.QSize(660, 270))
        self.__pte_ccc.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # frame to qle and btn
        lfrm_text = QtGui.QFrame()
        assert lfrm_text

        # setup
        lfrm_text.setAutoFillBackground(True)
        lfrm_text.setFrameShape(QtGui.QFrame.Panel)
        lfrm_text.setFrameShadow(QtGui.QFrame.Raised)

        # lineEdit command
        self.qle_ccc = QtGui.QLineEdit(lfrm_text)
        assert self.qle_ccc

        self.qle_ccc.setEnabled(True)
        self.qle_ccc.setText("")

        # bottom send command
        self.btn_send_ccc = QtGui.QPushButton("Send", lfrm_text)
        assert self.btn_send_ccc

        self.btn_send_ccc.setEnabled(False)

        # layout to frame
        llay_frm = QtGui.QHBoxLayout(lfrm_text)
        assert llay_frm is not None

        # setup
        llay_frm.setMargin(0)
        llay_frm.setSpacing(0)
        llay_frm.addWidget(self.qle_ccc)
        llay_frm.addWidget(self.btn_send_ccc)

        # create horizontal layout
        llay_gbx = QtGui.QVBoxLayout()
        assert llay_gbx is not None

        # put CCC on layout
        llay_gbx.addWidget(self.__pte_ccc)
        llay_gbx.addWidget(lfrm_text)

        # create groupBox altimeter
        lgbx_ccc = QtGui.QGroupBox(u"Comando/Controle/Configuração", self)
        assert lgbx_ccc

        # setup
        lgbx_ccc.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        lgbx_ccc.setLayout(llay_gbx)

        # return
        return lgbx_ccc

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_sns(self):
        """
        create sensors groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setFamily("Courier")
        l_font.setPointSize(12)

        # create QPlainTextEdit sensor
        self.__pte_sensor = QtGui.QPlainTextEdit()
        assert self.__pte_sensor

        self.__pte_sensor.setFont(l_font)
        self.__pte_sensor.setReadOnly(True)
        self.__pte_sensor.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_sensor.setMinimumSize(QtCore.QSize(500, 270))
        self.__pte_sensor.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put altimeter on layout
        llay_gbx.addWidget(self.__pte_sensor)

        # create groupBox altimeter
        lgbx_sns = QtGui.QGroupBox(u"Sensores", self)
        assert lgbx_sns

        # setup
        lgbx_sns.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        lgbx_sns.setLayout(llay_gbx)

        # return
        return lgbx_sns

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_config(self):
        """
        create configuration groupBox
        """
        # create font
        l_font = QtGui.QFont()
        assert l_font

        # setup
        l_font.setFamily("Courier")
        l_font.setPointSize(12)

        # create QPlainTextEdit configuração
        self.__pte_editor = QtGui.QPlainTextEdit()
        assert self.__pte_editor

        self.__pte_editor.setFont(l_font)
        self.__pte_editor.setReadOnly(False)
        self.__pte_editor.setStyleSheet(gdefs.D_PTE_STYLE)
        self.__pte_editor.setMinimumSize(QtCore.QSize(660, 270))
        self.__pte_editor.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # syntax highlight
        self.__highlight = sntx.CConfigHighlighter(self.__pte_editor.document())
        assert self.__highlight

        self.__pte_editor.show()

        # connections
        self.__pte_editor.textChanged.connect(self.on_pte_editor_textChanged)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None

        # put altimeter on layout
        llay_gbx.addWidget(self.__pte_editor)

        # create groupBox configuração
        lgbx_cnf = QtGui.QGroupBox(u"Configuração", self)
        assert lgbx_cnf

        # setup
        lgbx_cnf.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout
        lgbx_cnf.setLayout(llay_gbx)

        # return
        return lgbx_cnf

    # ---------------------------------------------------------------------------------------------
    def __create_toolbar(self, f_parent):
        """
        create toolbar
        """
        # check input
        assert f_parent
        
        # create toolBar
        ltbr_nmon = f_parent.addToolBar(self.tr("netMonitor"))
        assert ltbr_nmon is not None

        # new
        ltbr_nmon.addAction(f_parent.create_action(self.tr("&New"), f_shortcut="Ctrl+N",
            f_icon="new.png", f_slot=self.on_actionSave, f_tip=self.tr("New configuration")))

        # open
        ltbr_nmon.addAction(f_parent.create_action(self.tr("&Open"), f_shortcut="Ctrl+O",
            f_icon="open.png", f_slot=self.on_actionOpen, f_tip=self.tr("Open configuration")))

        # separator
        ltbr_nmon.addSeparator()

        # save
        ltbr_nmon.addAction(f_parent.create_action(self.tr("&Save"), f_shortcut="Ctrl+S",
            f_icon="save.png", f_slot=self.on_actionSave, f_tip=self.tr("Save configuration")))

        # save as
        ltbr_nmon.addAction(f_parent.create_action(self.tr("Save &As"), f_shortcut="Ctrl+A",
            f_icon="save.png", f_slot=self.on_actionSaveAs, f_tip=self.tr("Save configuration with another name")))

        # return
        return ltbr_nmon

    # ---------------------------------------------------------------------------------------------
    def __load_config_file(self, fs_file_path=None):
        """
        load configuration file
        """
        # don't receive fs_file_path ?
        if fs_file_path is None:
            # get last configuration file in use
            l_config = str(self.__settings.value("lastConfig").toString())

            # set file path
            fs_file_path = l_config if l_config else "papical.cfg"

        # flag ok
        lv_ok = False

        # create file object
        l_file = QtCore.QFile(fs_file_path)
        assert l_file

        # open file ok ?
        if l_file.open(QtCore.QIODevice.ReadOnly):
            # load text stream
            l_textStream = QtCore.QTextStream(l_file)
            assert l_textStream

            # put text on widget
            self.__pte_editor.setPlainText(l_textStream.readAll())

            # update settings
            self.__update_config_file_path(fs_file_path)

            # ok
            lv_ok = True

        # error in loading file ?
        if not lv_ok:
            # show message box
            self.__message("critical", "Could not load file: {}".format(fs_file_path))

        # return
        return lv_ok

    # ---------------------------------------------------------------------------------------------
    def __message(self, fs_type, fs_text):
        """
        show a message
        """
        # critical message box ?
        if "critical" == fs_type:
            # show message box
            QtGui.QMessageBox.critical(self, "", fs_text)

        # senão,...
        else:
            # show message box
            QtGui.QMessageBox.information(self, "", fs_text)

    # ---------------------------------------------------------------------------------------------
    def __save_config_file(self, fs_file_path):
        """
        save configuration file
        """
        # set ok flag
        lv_ok = False

        # create file handler
        l_file = QtCore.QFile(fs_file_path)
        assert l_file

        # open file ok ?
        if l_file.open(QtCore.QIODevice.WriteOnly):
            # create stream from file   
            l_textStream = QtCore.QTextStream(l_file)
            assert l_textStream

            # save text to file
            l_textStream << self.__pte_editor.toPlainText()
            l_textStream.flush()

            # reset dirty flag
            self.__v_config_file_is_dirty  = False

            # update config_file file path
            self.__update_config_file_path(fs_file_path)

            # ok
            lv_ok = True

        # any error ?
        if not lv_ok:
            # show error message
            # QtGui.QMessageBox.critical(self, "", "Could not save file: {}".format(fs_file_path), QtGui.QMessageBox.Ok)
            self.__message("critical", "Could not save file: {}".format(fs_file_path))
            
        # senão,...
        else:
            # update status bar
            self.__parent.statusBar().showMessage("File saved", 2000)

            # update status bar
            # self.__lbl_status.setText("Monitor idle")

        # return ok flag 
        return lv_ok

    # ---------------------------------------------------------------------------------------------
    def __update_config_file_path(self, fs_file_path):
        """
        update settings
        """
        # actual config
        self.__s_config_file_path = fs_file_path

        # save on settings
        self.__settings.setValue("lastConfig", fs_file_path)

        # set title
        self.__gbx_cnf.setTitle("Config file: {}".format(QtCore.QFileInfo(fs_file_path).fileName()))

        # flag dirty
        self.__v_config_file_is_dirty = False

    # =============================================================================================
    # callbacks
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    def on_actionNew(self):
        """
        new configuration action
        """
        # config_fileo ok ?
        if self.__check_config_file():
            # clear editor
            self.__pte_editor.clear()
            # clear file path
            self.__s_config_file_path = ""
            # show file path on status bar
            self__parent.statusBar().showMessage(self.__s_config_file_path)
            # reset flag dirty
            self.__v_config_file_is_dirty = False

    # ---------------------------------------------------------------------------------------------
    def on_actionOpen(self):
        """
        open configuration action
        """
        # config_fileo ok ?
        if not self.__check_config_file():
            # return
            return

        # get file path
        ls_file_path = str(QtGui.QFileDialog.getOpenFileName(self, self.tr("Open File"),
                       self.__s_config_file_path, self.tr("PAPI Calibra Configuration (*.cfg);;All Files (*)")))

        # file path ok ?
        if (ls_file_path is not None) and ("" != ls_file_path):
            # load configuration
            self.__load_config_file(ls_file_path)
    '''
    # ---------------------------------------------------------------------------------------------
    def on_actionRun_triggered(self):

        self.__config.parse( self.__pte_editor.toPlainText())
        self.dataText.setMaximumBlockCount(MAX(1, self.__config.get("_setup_", "width").toInt()))

        self.chart.init(self.__config)
        self.actionRun.setEnabled(False)
        self.actionStop.setEnabled(True)
        self.sendButton.setEnabled(True)
        self.dataText.clear()
    '''
    # ---------------------------------------------------------------------------------------------
    def on_actionSave(self):
        """
        save config_file action
        """
        # don't have file path ?
        if self.__s_config_file_path is None:
            # saveAs instead
            self.on_actionSaveAs()

        # senão,...
        else:
            # save config_file
            self.__save_config_file(self.__s_config_file_path)

    # ---------------------------------------------------------------------------------------------
    def on_actionSaveAs(self):
        """
        save as action
        """
        # get file path
        ls_file_path = str(QtGui.QFileDialog.getSaveFileName(self, self.tr("Save File"),
                       self.__s_config_file_path, self.tr("PAPI Calibra Configuration (*.cfg);;All Files (*)")))

        # have file path ?
        if (ls_file_path is not None) and ("" != ls_file_path):
            # save config_file
            self.__save_config_file(ls_file_path)
    '''
    # ---------------------------------------------------------------------------------------------
    def on_actionStop_triggered(self):

        self.actionStop.setEnabled(False)
        self.sendButton.setEnabled(False)
    '''
    # ---------------------------------------------------------------------------------------------
    def on_actionToolbar(self, fv_val):
        """
        toolbar visible action
        """
        self.__tbr_nmon.setVisible(fv_val)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def on_pte_editor_textChanged(self):
        """
        change in config file
        """
        # set dirty flag
        self.__v_config_file_is_dirty = True

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_camera(self, fs_msg):
        """
        message from camera
        """
        # put text on textEditor
        self.__pte_camera.appendPlainText(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_ccc(self, fs_msg):
        """
        message of command/control/config
        """
        # put text on textEditor
        self.__pte_ccc.appendPlainText(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def __on_msg_sensor(self, fs_msg):
        """
        message from sensors
        """
        # put text on textEditor
        self.__pte_sensor.appendPlainText(fs_msg)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page activated
        """
        self.__tbr_nmon.setEnabled(fv_on)
        self.__tbr_nmon.setVisible(fv_on)
    '''
    # ---------------------------------------------------------------------------------------------
    def on_sendButton_clicked(self):

        if self.__v_portValid:
            port.send(self.sendText.text())
    '''
# < the end >--------------------------------------------------------------------------------------
