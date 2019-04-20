#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_thermometer_feed

thermometer feed

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import threading
import time

# pyQt4
from PyQt4 import QtCore

# model
import model.pc_data as gdata
import model.pc_sensor_feed as snsf

# control
import control.pc_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CThermometerFeed >-----------------------------------------------------------------------------

class CThermometerFeed(snsf.CSensorFeed):
    """
    thermometer feed
    """
    # signal
    C_SGN_DATA_THR = QtCore.pyqtSignal(list)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_monitor=None):
        """
        constructor

        @param f_monitor: data monitor
        """ 
        # check input
        # assert f_monitor

        # network interface
        lt_ifc = gdata.G_DCT_CONFIG["net.ifc"]
        # network address
        ls_addr = gdata.G_DCT_CONFIG["net.adr"]
        # port
        li_port = int(gdata.G_DCT_CONFIG["net.thr"])

        # init super class
        super(CThermometerFeed, self).__init__(lt_ifc, ls_addr, li_port, f_monitor)

        # from CSensorFeed
        # sck_rcv     # receive socket
        # monitor     # data monitor
        # v_paused    # flag paused (bool)

        # make connections
        self.C_SGN_NEW_MSG_SNS.connect(self.trata_msg)

        # create receive data process
        l_prc = threading.Thread(target=self.query_data)
        assert l_prc

        # start process
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def trata_msg(self, fs_msg):
        """
        trata mensagem recebida

        @param fs_msg: received message
        """ 
        # check input
        assert fs_msg

        # monitor exists ?
        if self.monitor:
            # send message to monitor
            self.monitor.C_SGN_NEW_MSG_SNS.emit(str(fs_msg))

        # split message
        llst_msg = str(fs_msg).split('#')
        
        # valid thermometer message ?
        if (gdefs.D_MSG_VRS == int(llst_msg[0])) and (gdefs.D_MSG_THR == int(llst_msg[1])):
            # emit new thermometer data signal
            self.C_SGN_DATA_THR.emit(llst_msg[2:])

# < the end >--------------------------------------------------------------------------------------
