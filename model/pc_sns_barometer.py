#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sns_barometer

PAPI sender sensors

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

# numPy
import numpy as np

# model
import model.pc_kalman_filter_linear as kfl

# control
import control.pc_defs as gdefs
import control.pc_net_sock_out as nsck

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < CBarometer >-----------------------------------------------------------------------------------

class CBarometer(object):
    """
    barometer class
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ft_ifc, fs_addr, fi_port):
        """
        constructor

        @param ft_ifc: network interface
        @param fs_addr: client address
        @param fi_port: port
        """
        # check input
        assert fs_addr
        assert fi_port
                        
        # receive socket
        self.__sck_snd = nsck.CNetSockOut(ft_ifc, fs_addr, fi_port)
        assert self.__sck_snd
        
        # save client tuple
        self.__t_client = (fs_addr, fi_port)

        # how many sensors ?
        li_sensors = 2
        
        # state transition model
        l_A = np.matrix([[1.]])

        # control matrix
        l_B = np.matrix([[0.]])

        # control vector
        self.__u = np.matrix([[0.]])

        # observation matrix is the identity matrix, since we can get direct
        # measurements of all values in our example
        l_H = np.ones((li_sensors, 1))
        # print "l_H:", l_H, l_H.shape

        # initial covariance estimate
        l_P = np.ones(1)
        
        # process noise covariance (estimated error in process)
        l_Q = np.matrix([[0.005]])

        # measurement noise covariances (estimated error in measurements)
        l_R = np.eye(li_sensors) * 0.64
        # print "l_R:", l_R, l_R.shape

        # initial guess
        l_x = [[0.]]

        # create Kalman filter
        self.__kf = kfl.CKalmanFilterLinear(l_A, l_B, l_H, l_x, l_P, l_Q, l_R)
        assert self.__kf

    # ---------------------------------------------------------------------------------------------
    def send_data(self, lf_prs1, lf_prs2, lf_ts):
        """
        send barometer data
        """
        # save kalman state
        l_ks = self.__kf.get_current_state()

        # list or matrix ?
        lf_ks = l_ks[0][0] if list == type(l_ks) else l_ks[0, 0]

        # build string data
        ls_data = "{}#{}#{}#{}".format(lf_ts, lf_prs1, lf_prs2, lf_ks)

        # envia a string
        self.__sck_snd.sendto("{}#{}#{}".format(gdefs.D_MSG_VRS, gdefs.D_MSG_BAR, ls_data), self.__t_client)

        # step. control vector, measurement_vector
        self.__kf.step(self.__u, np.matrix([[lf_prs1], 
                                            [lf_prs2]]))

# < the end >--------------------------------------------------------------------------------------
