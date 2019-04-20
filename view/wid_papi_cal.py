#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_papi_cal

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

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.pc_camera_feed as camfd

# view
import view.wid_camera as wcam
import view.wid_papi_light_box as wplb
import view.wid_plot_papi as wplp

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CWidgetPAPICal >-------------------------------------------------------------------------------

class CWidgetPAPICal(QtGui.QWidget):
    """
    a port packet monitor that plots live data using PyQwt
    """
    # signal
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
        super(CWidgetPAPICal, self).__init__(f_parent)

        # parent
        self.__parent = f_parent
        
        # create camera groupBox
        lgbx_cam = self.__create_gbx_cam(f_control, f_monitor)

        # create plot groupBox
        lgbx_plp = self.__create_gbx_plot()

        # create lightBox groupBox
        lgbx_lbx = self.__create_gbx_light_box()

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes
        llo_grid.addWidget(lgbx_cam, 0, 0, 1,  1)
        llo_grid.addWidget(lgbx_plp, 0, 1, 1,  1)
        llo_grid.addWidget(lgbx_lbx, 1, 0, 1, -1)

        # make connections
        self.C_SGN_DATA_ALT.connect(self.__on_data_alt)
        self.C_SGN_PAGE_ON.connect(self.__on_page_on)

    # ---------------------------------------------------------------------------------------------
    def addToolBar(self, fs_title):
        """
        create toolBbar
        """
        return self.__parent.addToolBar(fs_title)

    # ---------------------------------------------------------------------------------------------
    def create_action(self, fs_title, **kwargs):
        """
        create action
        """
        return self.__parent.create_action(fs_title, **kwargs)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_cam(self, f_control, f_monitor):
        """
        create camera groupBox
        """
        # check input
        assert f_control
        assert f_monitor

        # create camera feed
        lcam_feed = camfd.CCameraFeed(f_control, f_monitor)
        assert lcam_feed

        # create camera widget
        lwid_camera = wcam.CWidgetCamera(lcam_feed, self)
        assert lwid_camera

        # create horizontal layout
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put camera on layout 
        llay_gbx.addWidget(lwid_camera)

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
    def __create_gbx_light_box(self):
        """
        create lightBox groupBox
        """
        # create the lightBoxes
        self.__lst_boxes = [wplb.CPAPILightBoxWidget("Caixa {}".format(i+1), self) for i in xrange(4)] 
        assert self.__lst_boxes 

        # place the horizontal panel widget
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # for all boxes... 
        for l_lbx in self.__lst_boxes:
            # put lightBox on layout
            llay_gbx.addWidget(l_lbx)

        # create groupBox lightBox
        lgbx_lightBox = QtGui.QGroupBox("Light Boxes", self)
        assert lgbx_lightBox

        # setup
        lgbx_lightBox.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_lightBox.setLayout(llay_gbx)

        # return
        return lgbx_lightBox

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_plot(self):
        """
        create plot groupBox
        """
        # create the plot and curves
        self.__wid_plp = wplp.CWidgetPlotPAPI(self) 
        assert self.__wid_plp 

        # place the horizontal panel widget
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # put plot on layout
        llay_gbx.addWidget(self.__wid_plp)

        # create groupBox plot
        lgbx_plot = QtGui.QGroupBox("Plot", self)
        assert lgbx_plot

        # setup
        lgbx_plot.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        lgbx_plot.setLayout(llay_gbx)

        # return
        return lgbx_plot
    
    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(list)
    def __on_data_alt(self, flst_data):
        """
        new altimeter data arrived
        """
        # for all boxes... 
        for l_lbx in self.__lst_boxes:
            # emit altimeter data signal
            l_lbx.C_SGN_DATA_ALT.emit(flst_data)

        # emit altimeter data signal
        self.__wid_plp.C_SGN_DATA_ALT.emit(flst_data)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page activated
        """
        if self.__wid_plp:
            self.__wid_plp.C_SGN_PAGE_ON.emit(fv_on)

# < the end >--------------------------------------------------------------------------------------
        