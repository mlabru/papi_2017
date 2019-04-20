#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
gbx_lateral_box

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

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CLateralBoxWidget >----------------------------------------------------------------------------

class CLateralBoxWidget(QtGui.QGroupBox):
    """
    a port packet monitor that plots live data using PyQwt
    """
    # signal
    #C_SGN_DATA_ALT = QtCore.pyqtSignal(list)
    #C_SGN_PAGE_ON = QtCore.pyqtSignal(bool)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_title, f_parent):
        """
        constructor

        @param fs_title: groupBox title
        @param f_parent: parent widget
        """
        # check input
        assert fs_title
        assert f_parent
        
        # init super class
        super(CLateralBoxWidget, self).__init__(fs_title, f_parent)

        # parent
        self.__parent = f_parent
        
        # events
        self.__event = f_parent.evtmgr
        assert self.__event

        # ângulos laterais
        self.__f_ang = 10.

        # create lateral groupBox
        self.__create_gbx_lateral(fs_title)

        # setup
        self.setMaximumWidth(90)
        self.setStyleSheet(gdefs.D_GBX_STYLE)

        # set groupBox layout 
        self.setLayout(self.__create_lay_1() if "Left" == fs_title else self.__create_lay_2())

        # make connections
        #self.C_SGN_DATA_ALT.connect(self.__on_data_alt)
        #self.C_SGN_PAGE_ON.connect(self.__on_page_on)

    # ---------------------------------------------------------------------------------------------
    def __create_gbx_lateral(self, fs_title):
        """
        create left groupBox
        """
        # create label graus
        self.__lbl_ang = QtGui.QLabel(u"{:4.2}°".format(self.__f_ang))
        assert self.__lbl_ang

        # setup
        self.__lbl_ang.setFont(QtGui.QFont("SansSerif", 13, QtGui.QFont.Bold))

        # create button left
        self.__btn_mark = QtGui.QPushButton(fs_title)
        assert self.__btn_mark

        # setup
        self.__btn_mark.setMinimumHeight(44)
        
        # make connections
        self.__btn_mark.clicked.connect(self.__on_btn_mark_clicked)

    # ---------------------------------------------------------------------------------------------
    def __create_lay_1(self):
        """
        create layout
        """
        # place the vertical widget
        llay_gbx = QtGui.QVBoxLayout()
        assert llay_gbx is not None
        
        # put config on layout
        llay_gbx.addWidget(self.__lbl_ang)
        llay_gbx.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        llay_gbx.addWidget(self.__btn_mark)

        # return
        return llay_gbx

    # ---------------------------------------------------------------------------------------------
    def __create_lay_2(self):
        """
        create layout
        """
        # place the vertical widget
        llay_gbx = QtGui.QGridLayout()
        assert llay_gbx is not None
        
        # put config on layout
        llay_gbx.addWidget(self.__lbl_ang,  0, 0, 1, 1)
        llay_gbx.addWidget(self.__btn_mark, 1, 0, 2, 1)

        # return
        return llay_gbx

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_mark_clicked(self):
        """
        pushButton mark clicked
        """
    '''
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
        self.__wid_plp.C_SGN_NEW_DIST.emit(ff_val)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def __on_page_on(self, fv_on):
        """
        page activated
        """
        # plot widget exists ?
        if self.__wid_plp:
            # emit page on signal
            self.__wid_plp.C_SGN_PAGE_ON.emit(fv_on)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_r2p(self, fi_box, ff_alt):
        """
        plot r2p activated
        """
        # plot widget exists ?
        if self.__wid_plp:
            # emit plot on signal
            self.__wid_plp.C_SGN_PLOT_R2P.emit(fi_box, ff_alt)

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(int, float)
    def __on_plot_p2w(self, fi_box, ff_alt):
        """
        plot p2w activated
        """
        # plot widget exists ?
        if self.__wid_plp:
            # emit plot on signal
            self.__wid_plp.C_SGN_PLOT_P2W.emit(fi_box, ff_alt)
    '''
    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    @property
    def evtmgr(self):
        return self.__event

# < the end >--------------------------------------------------------------------------------------
