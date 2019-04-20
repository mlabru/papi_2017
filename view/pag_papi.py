#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wid_papi

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
import view.gbx_camera as wcam
import view.gbx_config as wcfg
import view.gbx_lateral_box as wlbx
import view.gbx_papi_light_box as wplb
import view.gbx_plot_papi as wplp

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CPAPIWidget >-------------------------------------------------------------------------------

class CPAPIWidget(QtGui.QWidget):
    """
    a port packet monitor that plots live data using PyQwt
    """
    # signal
    C_SGN_DATA_ALT = QtCore.pyqtSignal(list)
    C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_monitor, f_parent):
        """
        constructor

        @param f_monitor: data monitor
        @param f_parent: parent widget
        """
        # check input
        assert f_monitor
        assert f_parent
        
        # init super class
        super(CPAPIWidget, self).__init__(f_parent)

        # parent
        self.__parent = f_parent
        
        # events
        self.__event = f_parent.evtmgr
        assert self.__event

        # create camera groupBox
        lgbx_cam = self.__create_gbx_cam(f_monitor)
        # create plot groupBox
        lgbx_plp = self.__create_gbx_plot()
        # create config groupBox
        lgbx_cfg = self.__create_gbx_config()
        # create lightBox groupBox
        lgbx_lbx = self.__create_gbx_light_box()

        # create frame layout
        llo_grid = QtGui.QGridLayout(self)
        assert llo_grid is not None

        # put all groupBoxes
        llo_grid.addWidget(lgbx_cam, 0, 0, 1,  1)
        llo_grid.addWidget(lgbx_plp, 0, 1, 1,  1)
        llo_grid.addWidget(lgbx_cfg, 0, 2, 1,  1)
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
    def __create_gbx_cam(self, f_monitor):
        """
        create camera groupBox
        """
        # check input
        assert f_monitor

        # create camera feed
        lcam_feed = camfd.CCameraFeed(f_monitor)
        assert lcam_feed

        # create camera widget
        lgbx_cam = wcam.CCameraWidget(u"Camera", lcam_feed, self)
        assert lgbx_cam

        # setup
        lgbx_cam.setStyleSheet(gdefs.D_GBX_STYLE)

        # return
        return lgbx_cam

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_config(self):
        """
        create config groupBox
        """
        # create the config and curves
        lgbx_config = wcfg.CConfigWidget("Config", self) 
        assert lgbx_config 

        # setup
        lgbx_config.setStyleSheet(gdefs.D_GBX_STYLE)

        # make connections
        lgbx_config.C_SGN_NEW_DIST.connect(self.__on_new_dist)

        # return
        return lgbx_config
    
    # ---------------------------------------------------------------------------------------------
    def __create_gbx_light_box(self):
        """
        create lightBox groupBox
        """
        # create the lightBoxes
        self.__lst_boxes = [wplb.CPAPILightBoxWidget("Caixa {}".format(cx + 1), cx, self) for cx in xrange(4)] 
        assert self.__lst_boxes 

        # place the horizontal panel widget
        llay_gbx = QtGui.QHBoxLayout()
        assert llay_gbx is not None
        
        # create left lateral widget
        lgbx_left = wlbx.CLateralBoxWidget("Left", self)
        assert lgbx_left

        # put left lateral widget on layout
        llay_gbx.addWidget(lgbx_left)

        # for all boxes... 
        for l_lbx in self.__lst_boxes:
            # make connections
            l_lbx.C_SGN_PLOT_R2P.connect(self.__on_plot_r2p)
            l_lbx.C_SGN_PLOT_P2W.connect(self.__on_plot_p2w)

            # put lightBox on layout
            llay_gbx.addWidget(l_lbx)

        # create right lateral widget
        lgbx_right = wlbx.CLateralBoxWidget("Right", self)
        assert lgbx_right

        # put right lateral widget on layout
        llay_gbx.addWidget(lgbx_right)

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
        self.__gbx_plot = wplp.CPlotPAPIWidget("Plot", self) 
        assert self.__gbx_plot 

        # setup
        self.__gbx_plot.setStyleSheet(gdefs.D_GBX_STYLE)

        # return
        return self.__gbx_plot
    
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

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    def __on_new_dist(self, ff_val):
        """
        new distance data arrived
        """
        # for all boxes... 
        for l_lbx in self.__lst_boxes:
            # emit distance data signal
            l_lbx.C_SGN_NEW_DIST.emit(ff_val)

        # emit distance data signal
        self.__gbx_plot.C_SGN_NEW_DIST.emit(ff_val)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page activated
        """
        # plot widget exists ?
        if self.__gbx_plot:
            # emit page on signal
            self.__gbx_plot.C_SGN_PAGE_ON.emit(fv_on)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_r2p(self, fi_box, ff_alt):
        """
        plot r2p activated
        """
        # plot widget exists ?
        if self.__gbx_plot:
            # emit plot on signal
            self.__gbx_plot.C_SGN_PLOT_R2P.emit(fi_box, ff_alt)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_p2w(self, fi_box, ff_alt):
        """
        plot p2w activated
        """
        # plot widget exists ?
        if self.__gbx_plot:
            # emit plot on signal
            self.__gbx_plot.C_SGN_PLOT_P2W.emit(fi_box, ff_alt)

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def evtmgr(self):
        return self.__event

# < the end >--------------------------------------------------------------------------------------
        