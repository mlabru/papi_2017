#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_camera_feed

camera feed

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

# numPy
import numpy as np

# openCV
import cv2
import cv2.cv as cv

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

# < CCameraFeed >----------------------------------------------------------------------------------

class CCameraFeed(snsf.CSensorFeed):
    """
    camera feed
    """
    # signal
    C_SGN_NEW_MSG_CAM = QtCore.pyqtSignal(str)
    C_SGN_DATA_FRAME  = QtCore.pyqtSignal(cv.iplimage)

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_monitor=None):
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
        li_port = int(gdata.G_DCT_CONFIG["net.img"])

        # init super class
        super(CCameraFeed, self).__init__(lt_ifc, ls_addr, li_port, f_monitor)

        # from CSensorFeed
        # sck_rcv     # receive socket
        # monitor     # data monitor
        # v_paused    # flag paused (bool)

        # make connections
        self.C_SGN_NEW_MSG_CAM.connect(self.dispatch_msg)

        # cria o processo de recebimento de imagens
        l_prc = threading.Thread(target=self.query_frame)
        assert l_prc

        # inicia o processo
        l_prc.start()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def dispatch_msg(self, fs_msg):
        """
        dispatch de imagens
        """
        # existe monitor ?
        if self.monitor:
            # envia mensagem ao monitor
            self.monitor.C_SGN_NEW_MSG_CAM.emit(fs_msg)

    # ---------------------------------------------------------------------------------------------
    def __receive_msg(self, f_sock, fi_size, fi_type):
        """
        receive a message
        """
        try:
            # receive image size
            l_msg, l_addr = f_sock.recvfrom(fi_size)

        # em caso de erro...
        except socket.error, l_err:
            # ger error code
            li_err = l_err.args[0]

            # no data available ?
            if (errno.EAGAIN == li_err) or (errno.EWOULDBLOCK == li_err):
                # no data available
                return False, None, None

            # senão,...
            else:
                # logger
                l_log = logging.getLogger("CCameraFeed::__receive_msg")
                l_log.setLevel(logging.CRITICAL)
                l_log.critical(u"<E01: error: {}".format(l_err))

                # a "real" error occurred
                sys.exit(1)

        # zero len message ?
        if 0 == len(l_msg):
            # logger
            l_log = logging.getLogger("CCameraFeed::__receive_msg")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: error: zero len message.")

            # continue
            return False, None, None

        # emit new message signal
        self.C_SGN_NEW_MSG_CAM.emit(l_msg)

        # split message
        llst_msg = l_msg.split('#')
        
        # mensagem inválida ?
        if (gdefs.D_MSG_VRS != int(llst_msg[0])) or (fi_type != int(llst_msg[1])):
            # return error
            return False, None, None

        # return message
        return True, llst_msg, l_msg

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def query_frame(self):
        """
        processo de recebimento de imagens
        """
        # clear to go
        assert self.sck_rcv

        # application wait
        while not gdata.G_KEEP_RUN:
            # aguarda
            time.sleep(1)

        # application loop
        while gdata.G_KEEP_RUN:
            # paused ?
            if self.v_paused:
                # aguarda
                time.sleep(1)
                # continua
                continue

            # non-blocking socket
            self.sck_rcv.settimeout(0.)
            self.sck_rcv.setblocking(0)

            # receive image size
            lv_ok, llst_msg, _ = self.__receive_msg(self.sck_rcv, 32, gdefs.D_MSG_SIZ)
            
            # invalid message ?
            if not lv_ok:
                # next message 
                continue
            
            # tamanho da mensagem
            li_len = int(llst_msg[2])

            # change to blocking socket
            self.sck_rcv.setblocking(1)

            # receive image
            lv_ok, llst_msg, l_msg = self.__receive_msg(self.sck_rcv, li_len, gdefs.D_MSG_IMG)
            
            # invalid message ?
            if not lv_ok:
                # next message 
                continue

            # calc offset to image start byte
            li_offset = len(llst_msg[0]) + len(llst_msg[1]) + 2

            # converte de string para imagem
            l_data = np.fromstring(l_msg[li_offset:], dtype="uint8")

            # decodifica a imagem
            l_data = cv2.imdecode(l_data, 1)

            # converting from numPy to iplImage
            l_frame = cv.CreateImageHeader((l_data.shape[1], l_data.shape[0]), cv.IPL_DEPTH_8U, 3)
            assert l_frame
            
            cv.SetData(l_frame, l_data.tostring(), l_data.dtype.itemsize * 3 * l_data.shape[1])

            # emit new frame signal
            self.C_SGN_DATA_FRAME.emit(l_frame)

        # fecha a conexão
        self.sck_rcv.close()

# < the end >--------------------------------------------------------------------------------------
