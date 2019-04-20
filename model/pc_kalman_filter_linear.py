#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
kalman_filter_linear

implements a multi-variable linear discrete Kalman filter

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"
    
# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# numPy
import numpy

# < class CKalmanFilterLinear >--------------------------------------------------------------------

class CKalmanFilterLinear(object):
    """
    implements a linear discrete Kalman filter
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, _A, _B, _H, _x, _P, _Q, _R):
        """
        constructor
        """
        self.A = _A    # state transition matrix
        self.B = _B    # control matrix
        self.H = _H    # observation matrix
        self.x = _x    # initial state estimate
        self.P = _P    # initial covariance estimate
        self.Q = _Q    # estimated error in process
        self.R = _R    # estimated error in measurements

    # ---------------------------------------------------------------------------------------------
    def get_current_state(self):
        """
        return current state
        """
        return self.x

    # ---------------------------------------------------------------------------------------------
    def step(self, f_u, f_z):
        """
        Kalman filter update
        
        @param f_u: control vector
        @param f_z: measurement_vector
        """
        # time update (prediction step)

        # (1) project the state ahead
        l_xhat = self.A * self.x + self.B * f_u

        # (2) project the error covariance ahead
        l_Pk = (self.A * self.P) * numpy.transpose(self.A) + self.Q

        # observation step
        l_innovation = f_z - self.H * l_xhat
        l_innovation_cov = self.H * l_Pk * numpy.transpose(self.H) + self.R

        # measurement update (update step)

        # (1) compute the Kalman gain
        l_Kk = l_Pk * numpy.transpose(self.H) * numpy.linalg.inv(l_innovation_cov)

        # (2) update estimate with measurement zk
        self.x = l_xhat + l_Kk * l_innovation

        # we need the size of the matrix so we can make an identity matrix
        li_size = self.P.shape[0]

        # (3) update the error covariance (eye(n) = n x n identity matrix)
        self.P = (numpy.eye(li_size) - l_Kk * self.H) * l_Pk

# < the end >--------------------------------------------------------------------------------------
