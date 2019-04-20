#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_wnd_main_cli

papi calibrate

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import csv
import glob
import logging
import os
import Queue
import random
import serial
import sys
import time

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_data as gdata
import model.pc_utils as util

# view
import view.pag_sensors as swid
import view.pag_monitor_net as mwid
import view.pag_papi as spap

# control
import control.events.events_basic as events

# resources
import view.resources_qrc

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPICalWndMainGCS >---------------------------------------------------------------------------

class CPAPICalWndMainGCS(QtGui.QMainWindow):
    """
    a port packet monitor that plots live data using PyQwt

    the monitor expects to receive 8 bytes data packets with a line return as a packet EOF on the
    serial port. Each received packet is analysed to extract gx, gy and gz.

    when the monitor is active, you can turn the 'Update speed' knob to control the frequency of
    screen updates.
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        """
        # check input
        assert f_control
        
        # init super class
        super(CPAPICalWndMainGCS, self).__init__()

        # control
        # self.__control = f_control
        # assert self.__control

        # dicionário de configuração
        # self.__dct_config = f_control.dct_config
        # assert self.__dct_config

        # model
        # self.__model = f_control.model
        # assert self.__model

        # event manager
        self.__event = f_control.event
        assert self.__event

        # register as event listener
        self.__event.register_listener(self)

        # live data feed
        # self.__live_feed = self.__model.live_feed
        # assert self.__live_feed

        # load settings
        l_settings = QtCore.QSettings("sophosoft", "papi_calibra")
        assert l_settings

        # create main Ui
        self.__setup_ui(l_settings)
        self.__create_toolbars()
        self.__create_status_bar()

        # update timer
        # self.__timer_update = QtCore.QTimer()
        # assert self.__timer_update

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(QtGui.QCloseEvent)
    def closeEvent(self, f_evt):
        """
        callback close event
        """
        # really quit ?
        if self.__really_quit():
            # load settings
            l_settings = QtCore.QSettings("sophosoft", "papi_calibra")
            assert l_settings

            # save actual config
            l_settings.setValue("pos", self.pos())
            l_settings.setValue("size", self.size())

            # accept
            f_evt.accept()

            # create CQuit event
            l_evt = events.CQuit()
            assert l_evt

            # dispatch event
            self.__event.post(l_evt)

        # otherwise, continua...
        else:
            # ignore
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    def create_action(self, f_text, f_slot=None, f_shortcut=None, f_icon=None, f_tip=None, f_checkable=False, f_signal="triggered()"):
        """
        create action
        """
        # create action
        l_action = QtGui.QAction(f_text, self)
        assert l_action

        # icon ?
        if f_icon is not None:
            # create icon
            l_icon = QtGui.QIcon()
            assert l_icon

            # convert pixmap
            l_icon.addPixmap(QtGui.QPixmap(":/images/{}".format(f_icon)))

            # set icon
            l_action.setIcon(l_icon)

        # shortcut ?
        if f_shortcut is not None:
            # set shortcut
            l_action.setShortcut(f_shortcut)

        # tip ?
        if f_tip is not None:
            # set tooltip
            l_action.setToolTip(f_tip)
            l_action.setStatusTip(f_tip)

        # slot ?
        if f_slot is not None:
            # make connection
            self.connect(l_action, QtCore.SIGNAL(f_signal), f_slot)

        # checkable ?
        if f_checkable:
            # set checkable
            l_action.setCheckable(True)

        # return
        return l_action

    # ---------------------------------------------------------------------------------------------
    def __create_status_bar(self):
        """
        create status bar
        """
        # create label status
        llbl_status = QtGui.QLabel("Monitor idle")
        assert llbl_status
         
        # put label on status bar
        self.statusBar().addWidget(llbl_status, 1)

    # ---------------------------------------------------------------------------------------------
    def __create_toolbars(self):
        """
        create toolbars
        """
        # create toolBar base
        ltbr_base = self.addToolBar(self.tr("Base"))
        assert ltbr_base is not None
        
        # exit
        ltbr_base.addAction(self.create_action(self.tr("E&xit"), f_shortcut="Ctrl+X", f_icon="quit.png",
                            f_slot=self.close, f_tip=self.tr("Exit the application")))

        #ltbr_base.addAction(self.__act_pause)
        
        # about
        ltbr_base.addAction(self.create_action(self.tr("&About"), f_shortcut="F1", 
                            f_slot=self.__on_about, f_tip=self.tr("About PAPI Calibra")))

        # about Qt
        ltbr_base.addAction(self.create_action(self.tr("About &Qt"),
                            f_slot=QtGui.qApp.aboutQt, f_tip=self.tr("About Qt")))

    # ---------------------------------------------------------------------------------------------
    # @staticmethod
    def notify(self, f_evt):
        """
        event handling callback

        @param f_event: received event
        """
        # check input
        assert f_evt

        # received quit event ?
        #if isinstance(f_evt, events.CQuit):
            #pass
        
    # ---------------------------------------------------------------------------------------------
    def __on_about(self):
        """
        callback about button
        """
        # get about text
        ls_msg = __doc__
        
        # show message box
        QtGui.QMessageBox.about(self, "About the PAPI Calibra", ls_msg.strip())

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def __on_data_alt(self, flst_data):
        """
        new altimeter data arrived
        """
        # generate PAPI Cal widget signal
        self.__pag_pap.C_SGN_DATA_ALT.emit(flst_data)        
        
    # ---------------------------------------------------------------------------------------------
    def __on_qtw_papi_currentChanged(self, fi_ndx):
        """
        tabWidget page change callback
        """
        # emit signals
        if self.__pag_pap:
            self.__pag_pap.C_SGN_PAGE_ON.emit(0 == fi_ndx)

        if self.__pag_sns:
            self.__pag_sns.C_SGN_PAGE_ON.emit(1 == fi_ndx)

        if self.__pag_mon:
            self.__pag_mon.C_SGN_PAGE_ON.emit(2 == fi_ndx)

    # ---------------------------------------------------------------------------------------------
    def __really_quit(self):
        """
        show message to confirm if user wants really quit appliction
        """
        # show message box
        l_ret = QtGui.QMessageBox.warning(self, self.tr("PAPI Calibra"),
                    self.tr("Do you want to quit PAPI Calibra ?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        # return
        return QtGui.QMessageBox.Yes == l_ret

    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self, f_settings):
        """
        setup user interface
        """
        # clear to go
        assert f_settings

        # create widget monitor (network) page
        self.__pag_mon = mwid.CMonitorNetWidget(f_settings, self)
        assert self.__pag_mon

        # create widget sensors page
        self.__pag_sns = swid.CSensorsWidget(self.__pag_mon, self)
        assert self.__pag_sns

        # make connections
        self.__pag_sns.C_SGN_DATA_ALT.connect(self.__on_data_alt)

        # create widget PAPI page
        self.__pag_pap = spap.CPAPIWidget(self.__pag_mon, self)
        assert self.__pag_pap

        # create tabWidget
        self.qtw_papi = QtGui.QTabWidget(self)
        assert self.qtw_papi is not None
        
        # setup
        self.qtw_papi.setStyleSheet("background-color: rgb(180, 180, 180);")
        self.qtw_papi.currentChanged[int].connect(self.__on_qtw_papi_currentChanged)
        
        # put pages on tabWidget
        self.qtw_papi.addTab(self.__pag_pap, "PAPI")
        self.qtw_papi.addTab(self.__pag_sns, "Sensores")
        self.qtw_papi.addTab(self.__pag_mon, "Monitor")

        # create tab widget
        self.centralwidget = QtGui.QWidget()
        assert self.centralwidget

        # create layout
        l_vl = QtGui.QHBoxLayout(self.centralwidget)
        assert l_vl is not None
        
        # put tabWidget on layout
        l_vl.addWidget(self.qtw_papi)
        
        # set tabWidget as centralWidget
        self.setCentralWidget(self.centralwidget)

        # config main window
        self.setWindowTitle("PAPI Calibra [GCS] v0.1")

        # set position
        self.move(f_settings.value("pos", QtCore.QPoint(200, 200)).toPoint())

        # set size 
        self.resize(f_settings.value("size", QtCore.QSize(1024, 768)).toSize())

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def evtmgr(self):
        return self.__event
        
# < the end >--------------------------------------------------------------------------------------
