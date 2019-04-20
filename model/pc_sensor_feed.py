#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_sensor_feed

sensors feed

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/05"

# < imports >--------------------------------------------------------------------------------------

# python library
import errno
import logging
import socket
import threading
import time

# pyQt4
from PyQt4 import QtCore

# model
import model.pc_data as gdata

# control
import control.pc_defs as gdefs
import control.pc_net_sock_in as nsck

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CSensorFeed >----------------------------------------------------------------------------------

class CSensorFeed(QtCore.QObject):
    """
    sensors feed
    """
    # signal new message received
    C_SGN_NEW_MSG_SNS = QtCore.pyqtSignal(str)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifc, fs_addr, fi_port, f_monitor=None):
        """
        constructor

        @param ft_ifc: socket interface
        @param fs_addr: socket address
        @param fi_port: receive socket port
        """ 
        # check input
        assert ft_ifc
        assert fs_addr
        assert fi_port

        # init super class
        super(CSensorFeed, self).__init__()

        # receive socket
        self.__sck_rcv = nsck.CNetSockIn(ft_ifc, fs_addr, fi_port)
        assert self.__sck_rcv

        # data monitor
        self.__monitor = f_monitor

        # flag paused
        self.__v_paused = False

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def query_data(self):
        """
        processo de recebimento de dados
        """
        # clear to go
        assert self.__sck_rcv

        # non-blocking socket
        self.__sck_rcv.settimeout(0.)
        self.__sck_rcv.setblocking(0)

        # application wait
        while not gdata.G_KEEP_RUN:
            # aguarda
            time.sleep(1)

        # application loop
        while gdata.G_KEEP_RUN:
            # paused ?
            if self.__v_paused:
                # aguarda
                time.sleep(1)

                # continua
                continue

            try:
                # recebe uma mensagem (até 1024 bytes)
                l_msg, l_addr = self.__sck_rcv.recvfrom(1024)

            # em caso de erro...
            except socket.error, l_err:
                # ger error code
                li_err = l_err.args[0]

                # no data available ?
                if (errno.EAGAIN == li_err) or (errno.EWOULDBLOCK == li_err):
                    # no data available
                    continue

                # senão,...
                else:
                    # logger
                    l_log = logging.getLogger("CSensorFeed::query_data")
                    l_log.setLevel(logging.CRITICAL)
                    l_log.critical("<E01: pc_sensor_feed: {}".format(l_err))

                    # a "real" error occurred
                    sys.exit(1)

            # zero len message ?
            if 0 == len(l_msg):
                # logger
                l_log = logging.getLogger("CSensorFeed::query_data")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E02: pc_sensor_feed: zero len message.")

                # continue
                continue

            # senão,...
            else:
                # emit new message signal
                self.C_SGN_NEW_MSG_SNS.emit(l_msg)

        # fecha a conexão
        self.__sck_rcv.close()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def monitor(self):
        return self.__monitor

    @monitor.setter
    def monitor(self, f_val):
        self.__monitor = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_paused(self):
        return self.__v_paused

    @v_paused.setter
    def v_paused(self, f_val):
        self.__v_paused = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv(self):
        return self.__sck_rcv

    @sck_rcv.setter
    def sck_rcv(self, f_val):
        self.__sck_rcv = f_val

# < the end >--------------------------------------------------------------------------------------
