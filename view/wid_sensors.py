#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_sensors

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

# openCV
import cv2.cv as cv

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_altimeter_feed as altfd
import model.pc_barometer_feed as barfd
import model.pc_gps_feed as gpsfd
import model.pc_thermometer_feed as thrfd

# view
import view.wid_altimeter as walt
import view.wid_barometer as wbar
import view.wid_gps as wgps
import view.wid_thermometer as wthr

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetSensors >-------------------------------------------------------------------------------

class CWidgetSensors(QtGui.QWidget):
    """
    a port packet monitor that plots live data using PyQwt
    """
    # signals
    C_SGN_DATA_ALT = QtCore.pyqtSignal(list)
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_monitor, f_parent=None):
        """
        constructor

        @param f_control: control
        @param f_monitor: data monitor
        @param f_parent: parent widget
        """
        # check input
        assert f_control
        assert f_monitor
        
        # init super class
        super(CWidgetSensors, self).__init__(f_parent)

        # parent
        # self.__parent = f_parent
        
        # create altimeter groupBox
        lgbx_alt = self.__create_gbx_alt(f_control, f_monitor)

        # create GPS groupBox
        lgbx_gps = self.__create_gbx_gps(f_control, f_monitor)

        # create barameter groupBox
        lgbx_bar = self.__create_gbx_bar(f_control, f_monitor)

        # create thermometer groupBox
        lgbx_thr = self.__create_gbx_thr(f_control, f_monitor)

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes on a grid
        llo_grid.addWidget(lgbx_alt, 0, 0, 1, 1)
        llo_grid.addWidget(lgbx_gps, 0, 1, 1, 1)
        llo_grid.addWidget(lgbx_bar, 1, 0, 1, 1)
        llo_grid.addWidget(lgbx_thr, 1, 1, 1, 1)

        # connect new data signal
        self.C_SGN_PAGE_ON.connect(self.__on_page_on)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_alt(self, f_control, f_monitor):
        """
        create altimeter groupBox
        """
        # create altimeter feed
        lfeed_alt = altfd.CAltimeterFeed(f_control, f_monitor)
        assert lfeed_alt

        # create altimeter widget
        lwid_altimeter = walt.CWidgetAltimeter(lfeed_alt, self)
        assert lwid_altimeter

        # setup
        lwid_altimeter.setMaximumHeight(300)

        # make connections
        lwid_altimeter.C_SGN_DATA_ALT.connect(self.__on_data_alt)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put altimeter on layout 
        llay_gbx.addWidget(lwid_altimeter)

        # create groupBox altimeter
        lgbx_alt = QtGui.QGroupBox(u"Altímetro", self)
        assert lgbx_alt

        # setup
        lgbx_alt.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_alt.setLayout(llay_gbx)

        # return
        return lgbx_alt

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_bar(self, f_control, f_monitor):
        """
        create barometer groupBox
        """
        # create barometer feed
        lfeed_bar = barfd.CBarometerFeed(f_control, f_monitor)
        assert lfeed_bar

        # create barometer widget
        lwid_barometer = wbar.CWidgetBarometer(lfeed_bar, self)
        assert lwid_barometer

        # setup
        lwid_barometer.setMaximumHeight(300)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put barometer on layout 
        llay_gbx.addWidget(lwid_barometer)

        # create groupBox barometer
        lgbx_bar = QtGui.QGroupBox(u"Barômetro", self)
        assert lgbx_bar

        # setup
        lgbx_bar.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_bar.setLayout(llay_gbx)

        # return
        return lgbx_bar

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_gps(self, f_control, f_monitor):
        """
        create GPS groupBox
        """
        # create GPS feed
        lfeed_gps = gpsfd.CGPSFeed(f_control, f_monitor)
        assert lfeed_gps

        # create GPS widget
        lwid_gps = wgps.CWidgetGPS(lfeed_gps, self)
        assert lwid_gps

        # setup
        lwid_gps.setMaximumHeight(300)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put GPS on layout 
        llay_gbx.addWidget(lwid_gps)

        # create groupBox GPS
        lgbx_gps = QtGui.QGroupBox(u"GPS", self)
        assert lgbx_gps

        # setup
        lgbx_gps.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_gps.setLayout(llay_gbx)

        # return
        return lgbx_gps

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_thr(self, f_control, f_monitor):
        """
        create thermometer groupBox
        """
        # create thermometer feed
        lfeed_thr = thrfd.CThermometerFeed(f_control, f_monitor)
        assert lfeed_thr

        # create thermometer widget
        lwid_thermometer = wthr.CWidgetThermometer(lfeed_thr, self)
        assert lwid_thermometer

        # setup
        lwid_thermometer.setMaximumHeight(300)

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put thermometer on layout 
        llay_gbx.addWidget(lwid_thermometer)

        # create groupBox thermometer
        lgbx_thr = QtGui.QGroupBox(u"Termômetro", self)
        assert lgbx_thr

        # setup
        lgbx_thr.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_thr.setLayout(llay_gbx)

        # return
        return lgbx_thr

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def __on_data_alt(self, flst_data):
        """
        altimeter new data
        """
        # emit data_alt signal
        self.C_SGN_DATA_ALT.emit(flst_data)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page activated
        """
        return

# < the end >--------------------------------------------------------------------------------------
        