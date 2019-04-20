#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_wnd_main_srv

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
from PyQt4 import Qwt5

# model
import model.pc_data as gdata
import model.pc_utils as util

import model.tty_monitor as tmon

# view
import view.wid_calibra as cwid
import view.pag_sensors as swid
import view.wid_tty_monitor as twid

# control
import control.events.events_basic as events
import control.events.events_tty as evttty

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)
'''
M_GYRO_X = "gyro_x"
M_GYRO_Y = "gyro_y"
M_GYRO_Z = "gyro_z"
M_ACCL_X = "accel_x"
M_ACCL_Y = "accel_y"
M_ACCL_Z = "accel_z"
M_MAGN_X = "magn_x"
M_MAGN_Y = "magn_y"
M_MAGN_Z = "magn_z"

M_CURVES = [M_GYRO_X, M_GYRO_Y, M_GYRO_Z, \
            M_ACCL_X, M_ACCL_Y, M_ACCL_Z, \
            M_MAGN_X, M_MAGN_Y, M_MAGN_Z]
'''
# < CPAPICalWndMainSrv >---------------------------------------------------------------------------

class CPAPICalWndMainSrv(QtGui.QMainWindow):
    """
    a serial port packet monitor that plots live data using PyQwt

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
        # init super class
        super(CPAPICalWndMainSrv, self).__init__()

        # control
        self.__control = f_control
        assert self.__control

        # dicionário de configuração
        self.__dct_config = f_control.dct_config
        assert self.__dct_config

        # model
        self.__model = f_control.model
        assert self.__model

        # event manager
        #self.__event = f_control.event
        #assert self.__event

        # register as event listener
        #self.__event.register_listener(self)

        # live data feed
        self.__live_feed = self.__model.live_feed
        assert self.__live_feed

        # create main Ui
        self.__setup_ui()

        # config main window
        self.setWindowTitle("PAPI Calibra [Server] v0.1")
        self.resize(1255, 755)

        # config UI
        #self.__create_menu()
        self.__create_status_bar()

        # activate start-stop button connections
        #self.btn_start.clicked.connect(self.__on_start)
        #self.btn_stop.clicked.connect(self.__on_stop)

        # update timer
        self.__timer_update = QtCore.QTimer()
        assert self.__timer_update
    '''
    # ---------------------------------------------------------------------------------------------
    # the following two methods are utilities for simpler creation and assignment of actions

    def __add_actions(self, target, actions):
        """
        add actions
        """
        for action in actions:
            if action is None:
                target.addSeparator()

            else:
                target.addAction(action)

    # ---------------------------------------------------------------------------------------------
    def __create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        """
        create action
        """
        # create action
        action = QtGui.QAction(text, self)
        assert action

        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))

        if shortcut is not None:
            action.setShortcut(shortcut)

        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)

        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)

        if checkable:
            action.setCheckable(True)

        # return
        return action

    # ---------------------------------------------------------------------------------------------
    def __create_knob(self):
        """
        create a knob

        @return return a the knob widget
        """
        # create Qwt knob
        l_knob = Qwt5.QwtKnob(self)
        assert l_knob
        
        # setup knob
        l_knob.setRange(0, 180, 0, 1)
        l_knob.setScaleMaxMajor(10)
        l_knob.setKnobWidth(40)
        l_knob.setValue(10)

        # return
        return l_knob

    # ---------------------------------------------------------------------------------------------
    def __create_menu(self):
        """
        create menu
        """
        # file menu
        self.__mnu_file = self.menuBar().addMenu("&File")
        assert self.__mnu_file

        # select tty port...
        lact_select_tty = self.__create_action("Select TTY &Port...", shortcut="Ctrl+P", 
                                               slot=self.__on_select_port, tip="Select a TTY port")

        # start monitor
        self.__act_start = self.__create_action("&Start monitor", shortcut="Ctrl+M", 
                                                slot=self.__on_start, tip="Start the data monitor")
        self.__act_start.setEnabled(False)

        # stop monitor 
        self.__act_stop = self.__create_action("&Stop monitor", shortcut="Ctrl+T", 
                                               slot=self.__on_stop, tip="Stop the data monitor")
        self.__act_stop.setEnabled(False)

        # exit
        lact_exit = self.__create_action("E&xit", slot=self.close, 
                                         shortcut="Ctrl+X", tip="Exit the application")

        # put actions on file menu
        self.__add_actions(self.__mnu_file, (lact_select_tty, self.__act_start, self.__act_stop, None, lact_exit))

        # help menu
        self.__mnu_help = self.menuBar().addMenu("&Help")
        assert self.__mnu_help

        # about
        lact_about = self.__create_action("&About", shortcut="F1", 
                                          slot=self.__on_about, tip="About the monitor")

        # put actions on help menu
        self.__add_actions(self.__mnu_help, (lact_about,))
    '''
    # ---------------------------------------------------------------------------------------------
    def __create_status_bar(self):
        """
        create status bar
        """
        # create label status
        self.__lbl_status = QtGui.QLabel("Monitor idle")
        assert self.__lbl_status
         
        # put label on status bar
        self.statusBar().addWidget(self.__lbl_status, 1)
    '''
    # ---------------------------------------------------------------------------------------------
    def __fill_bauds_combo(self):
        """ 
        rescan the serial port com and update the combobox
        """
        # clear bauds comboBox
        self.cbx_baud.clear()

        # list of available bauds
        self.__lst_available_baud = [9600, 19200, 38400, 57600, 115200]

        # for all bauds
        for li_baud in self.__lst_available_baud:
            # put on comboBox
            self.cbx_baud.addItem(str(li_baud))

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_accel(self):
        """
        fill accelerometer groupBox
        """
        # create the plot and curves
        self.plot_acc, self.curve_acc = self.__create_plot("Acceleration", gdata.ACC_YMIN, gdata.ACC_YMAX)

        self.gCheckBox = [self.__create_checkbox("Acceleration(x)", QtCore.Qt.green,  self.__activate_curve, M_ACCL_X),
                          self.__create_checkbox("Acceleration(y)", QtCore.Qt.red,    self.__activate_curve, M_ACCL_Y),
                          self.__create_checkbox("Acceleration(z)", QtCore.Qt.yellow, self.__activate_curve, M_ACCL_Z)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_acc, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_accel.setLayout(llay_gbx)
        #self.gbx_accel.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_gyro(self):
        """
        fill gyroscope groupBox
        """
        # create the plot and curves
        self.plot_gyr, self.curve_gyr = self.__create_plot("Gyroscope", gdata.GYR_YMIN, gdata.GYR_YMAX)

        self.gCheckBox = [self.__create_checkbox("Gyroscope(x)", QtCore.Qt.green,  self.__activate_curve, M_GYRO_X),
                          self.__create_checkbox("Gyroscope(y)", QtCore.Qt.red,    self.__activate_curve, M_GYRO_Y),
                          self.__create_checkbox("Gyroscope(z)", QtCore.Qt.yellow, self.__activate_curve, M_GYRO_Z)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_gyr, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_gyro.setLayout(llay_gbx)
        #self.gbx_gyro.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_ir_1(self):
        """
        fill ir_1 groupBox
        """
        # create the plot and curves
        self.plot_ir1, self.curve_ir1 = self.__create_plot("Infrared 1", gdata.ACC_YMIN, gdata.ACC_YMAX)

        self.gCheckBox = [self.__create_checkbox("Infrared(x)", QtCore.Qt.green,  self.__activate_curve, 0),
                          self.__create_checkbox("Infrared(y)", QtCore.Qt.red,    self.__activate_curve, 1),
                          self.__create_checkbox("Infrared(z)", QtCore.Qt.yellow, self.__activate_curve, 2)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_ir1, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_ir_1.setLayout(llay_gbx)
        #self.gbx_ir_1.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_ir_2(self):
        """
        fill ir_2 groupBox
        """
        # create the plot and curves
        self.plot_ir2, self.curve_ir2 = self.__create_plot("Infrared 2", gdata.ACC_YMIN, gdata.ACC_YMAX)

        self.gCheckBox = [self.__create_checkbox("Infrared(x)", QtCore.Qt.green,  self.__activate_curve, 0),
                          self.__create_checkbox("Infrared(y)", QtCore.Qt.red,    self.__activate_curve, 1),
                          self.__create_checkbox("Infrared(z)", QtCore.Qt.yellow, self.__activate_curve, 2)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_ir2, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_ir_2.setLayout(llay_gbx)
        #self.gbx_ir_2.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_magn(self):
        """
        fill magnetometer groupBox
        """
        # create the plot and curves
        self.plot_mag, self.curve_mag = self.__create_plot("Magnetometer", gdata.MAG_YMIN, gdata.MAG_YMAX)

        self.gCheckBox = [self.__create_checkbox("Magneto(x)", QtCore.Qt.green,  self.__activate_curve, M_MAGN_X),
                          self.__create_checkbox("Magneto(y)", QtCore.Qt.red,    self.__activate_curve, M_MAGN_Y),
                          self.__create_checkbox("Magneto(z)", QtCore.Qt.yellow, self.__activate_curve, M_MAGN_Z)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_mag, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_magn.setLayout(llay_gbx)
        #self.gbx_magn.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_setup(self):
        """
        fill setup groupBox
        """
        # update speed knob
        self.__knb_update_freq = self.__create_knob()
        assert self.__knb_update_freq
        
        # connect knob value changed 
        self.__knb_update_freq.valueChanged.connect(self.__on_knob_change)

        # knob label
        self.__lbl_knob = QtGui.QLabel("Update speed = {} (Hz)".format(self.__knb_update_freq.value()))
        assert self.__lbl_knob

        # setup knob label
        self.__lbl_knob.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        # knob vertical box
        knob_vbox = QtGui.QVBoxLayout()
        assert knob_vbox is not None
         
        knob_vbox.addWidget(self.__knb_update_freq)
        knob_vbox.addWidget(self.__lbl_knob)
        # knob_vbox.addStretch(1)

        # create the configuration horizontal panel
        self.max_spin = QtGui.QSpinBox()
        assert self.max_spin
        
        self.max_spin.setMaximum(1000)
        self.max_spin.setValue(1000)

        # spins horizontal box
        spins_hbox = QtGui.QHBoxLayout()
        assert spins_hbox is not None
         
        spins_hbox.addWidget(QtGui.QLabel("Save every"))
        spins_hbox.addWidget(self.max_spin)
        spins_hbox.addWidget(QtGui.QLabel("Lines"))
        spins_hbox.addStretch(1)

        # place the horizontal panel widget
        # llay_gbx = QtGui.QGridLayout()
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put widgets on layout
        llay_gbx.addLayout(knob_vbox)
        llay_gbx.addLayout(spins_hbox)

        # setup gbx
        #self.gbx_setup.setLayout(llay_gbx)
        #self.gbx_setup.setFixedHeight(150)
        
    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_sonar(self):
        """
        fill sonar groupBox
        """
        # create the plot and curves
        self.plot_son, self.curve_son = self.__create_plot("Sonar", gdata.ACC_YMIN, gdata.ACC_YMAX)

        self.gCheckBox = [self.__create_checkbox("Sonar(x)", QtCore.Qt.green,  self.__activate_curve, 0),
                          self.__create_checkbox("Sonar(y)", QtCore.Qt.red,    self.__activate_curve, 1),
                          self.__create_checkbox("Sonar(z)", QtCore.Qt.yellow, self.__activate_curve, 2)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_son, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_sonar.setLayout(llay_gbx)
        #self.gbx_sonar.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_term(self):
        """
        fill termometer groupBox
        """
        # create the plot and curves
        self.plot_trm, self.curve_trm = self.__create_plot("Temperature", gdata.ACC_YMIN, gdata.ACC_YMAX)

        self.gCheckBox = [self.__create_checkbox("Temp(x)", QtCore.Qt.green,  self.__activate_curve, 0),
                          self.__create_checkbox("Temp(y)", QtCore.Qt.red,    self.__activate_curve, 1),
                          self.__create_checkbox("Temp(z)", QtCore.Qt.yellow, self.__activate_curve, 2)
                         ]

        # clear screen button
        lbtn_clear = QtGui.QPushButton("clear plot")
        assert lbtn_clear

        # connect clear screen button        
        lbtn_clear.clicked.connect(self.__clear_screen)

        # place the horizontal panel widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        llay_gbx.addWidget(self.plot_trm, 0, 0, 8, 7)
        llay_gbx.addWidget(self.gCheckBox[0], 0, 8)
        llay_gbx.addWidget(self.gCheckBox[1], 1, 8)
        llay_gbx.addWidget(self.gCheckBox[2], 2, 8)
        llay_gbx.addWidget(lbtn_clear, 3, 8)
        # llay_gbx.addStretch()

        #self.gbx_term.setLayout(llay_gbx)
        #self.gbx_term.setFixedHeight(300)

    # ---------------------------------------------------------------------------------------------
    def __fill_gbx_tty(self):
        """
        fill tty monitor groupBox
        """
        # fill ports combobox
        self.__fill_ports_combo()

        # fill bauds combobox
        self.__fill_bauds_combo()

        # disable stop button
        self.btn_stop.setEnabled(False)

        # config monitor groupBox
        #self.gbx_tty.setFixedHeight(150)
        #self.gbx_tty.setMinimumWidth(550)

    # ---------------------------------------------------------------------------------------------
    def __fill_ports_combo(self):
        """ 
        rescan the serial ports and update the combobox
        """
        # clear comboBox
        self.cbx_port.clear()

        # get list of available ports 
        self.__lst_available_tty = tmon.enumerate_serial_ports()

        # for all available ports...
        for ls_port in self.__lst_available_tty:
            # put port on comboBox
            self.cbx_port.addItem(ls_port)

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
        if isinstance(f_evt, events.CQuit):
            # wait all tasks terminate
            time.sleep(1)
            # ends application
            sys.exit()

    # ---------------------------------------------------------------------------------------------
    def __on_about(self):
        """
        callback about button
        """
        # get about text
        ls_msg = __doc__
        
        # show message box
        QtGui.QMessageBox.about(self, "About the serial plotter", ls_msg.strip())

    # ---------------------------------------------------------------------------------------------
    def __on_knob_change(self):
        """ 
        when the knob is rotated, it sets the update interval of the timer
        """
        # get knob value
        lf_update_freq = self.__knb_update_freq.value()

        # update text label 
        self.__lbl_knob.setText("Update speed = %s (Hz)" % self.__knb_update_freq.value())

        # update timer is active ?
        if self.__timer_update.isActive():
            # set new frequency
            lf_update_freq = max(0.01, lf_update_freq)
            # set timer interval
            self.__timer_update.setInterval(1000.0 / lf_update_freq)

    # ---------------------------------------------------------------------------------------------
    def __on_select_port(self):
        """
        DOCUMENT ME!
        """
        ports = enumerate_serial_ports()

        if len(ports) == 0:
            QMessageBox.critical(self, "No ports", "No serial ports found")
            return

        item, ok = QtGui.QInputDialog.getItem(self, "Select a port", "Serial port:", ports, 0, False)

        if ok and not item.isEmpty():
            self.portname.setText(item)
            self.set_actions_enable_state()

    # ---------------------------------------------------------------------------------------------
    def __on_start(self):
        """ 
        start the monitor: com_monitor thread and the update timer
        """
        # get port comboBox current index
        li_ndx = self.cbx_port.currentIndex()
        # get current selected port
        ls_port = self.__lst_available_tty[li_ndx]

        # get baud comboBox current index
        li_ndx = self.cbx_baud.currentIndex()
        # get current selected baud
        li_baud = self.__lst_available_baud[li_ndx]

        # disable start button
        self.btn_start.setEnabled(False)
        # enable stop button 
        self.btn_stop.setEnabled(True)
        # disable port comboBox
        self.cbx_port.setEnabled(False)
        # disable baud comboBox
        self.cbx_baud.setEnabled(False)

        # create TTYMonitorStart event
        l_evt = evttty.CTTYMonitorStart(ls_port, li_baud)
        assert l_evt

        # send event
        self.__event.post(l_evt)

        # config timer update method
        self.__timer_update.timeout.connect(self.__on_timer)

        # get update frequency
        lf_update_freq = self.__knb_update_freq.value()

        if lf_update_freq > 0:
            # start timer update
            self.__timer_update.start(1000. / lf_update_freq)

        # update statusBar
        self.__lbl_status.setText("Monitor running")

    # ---------------------------------------------------------------------------------------------
    def __on_stop(self):
        """ 
        stop the monitor
        """
        if self.com_monitor is not None:
            self.com_monitor.join(1000)
            self.com_monitor = None

        # reset flag
        self.monitor_active = False

        # enable start button
        self.btn_start.setEnabled(True)
        # disable stop button
        self.btn_stop.setEnabled(False)
        # enable tty port comboBox
        self.cbx_port.setEnabled(True)

        # stops update timer
        self.__timer_update.stop()

        # update status bar
        self.__lbl_status.setText("Monitor idle")

    # ---------------------------------------------------------------------------------------------
    def __on_timer(self):
        """ 
        executed periodically when the monitor update timer is fired
        """
        # create TTYMonitorUpdate event
        l_evt = evttty.CTTYMonitorUpdate()
        assert l_evt

        # send event
        self.__event.post(l_evt)

        # update
        self.update_monitor()

    # ---------------------------------------------------------------------------------------------
    def set_actions_enable_state(self):
        """
        set actions enable state
        """
        if "" == self.portname.text():
            lv_start_enable = lv_stop_enable = False

        else:
            lv_start_enable = not self.monitor_active
            lv_stop_enable = self.monitor_active

        self.__act_start.setEnabled(lv_start_enable)
        self.__act_stop.setEnabled(lv_stop_enable)
    '''
    # ---------------------------------------------------------------------------------------------
    def __setup_ui(self):
        """
        setup user interface
        """
        # clear to go
        assert self.__control

        # create tabWidget
        self.qtw_sensors = QtGui.QTabWidget(self)
        assert self.qtw_sensors is not None
        
        ### 
        # Calibração page
        
        # create tab widget
        lwid_cal = QtGui.QWidget()
        assert lwid_cal
        
        # create widget calibrate
        self.wid_cal = cwid.CWidgetCalibra(lwid_cal)
        assert self.wid_cal

        # put on tabWidget
        self.qtw_sensors.addTab(lwid_cal, u"Calibração")
        
        ### 
        # Monitor page

        # create tab widget
        lwid_mon = QtGui.QWidget()
        assert lwid_mon
        
        # create widget monitor (serial)
        self.wid_mon = twid.CWidgetTTYMonitor(lwid_mon)
        assert self.wid_mon

        # put on tabWidget
        self.qtw_sensors.addTab(lwid_mon, "Monitor")
            
        # create tab widget
        self.centralwidget = QtGui.QWidget()
        assert self.centralwidget

        # create layout
        l_vl = QtGui.QHBoxLayout(self.centralwidget)
        assert l_vl is not None
        
        # put tabWidget on layout
        l_vl.addWidget(self.qtw_sensors)
        
        # set tabWidget as centralWidget
        self.setCentralWidget(self.centralwidget)

# < the end >--------------------------------------------------------------------------------------
