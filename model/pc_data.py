#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
glb_data

global data

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < global data >----------------------------------------------------------------------------------

# canal de comunicação
G_CANAL = 4

# modo de execução (cliente(F)/servidor(T))
G_SERVER = False

# modo debug
G_DEBUG = False

# keep things running
G_KEEP_RUN = False

# configuration dictionary
G_DCT_CONFIG = {}

# ADXL345 constants
#EARTH_GRAVITY_MS2 = 9.80665
#SCALE_MULTIPLIER  = 0.0078

G_YMAX = 150  #  4.000
G_YMIN =  35  # -4.000

#ACC_YMAX =  200
#ACC_YMIN = -200

# altimeter plot widget
G_ALT_YMAX =  50
G_ALT_YMIN = -50

#GYR_YMAX =  50
#GYR_YMIN = -50

#MAG_YMAX =  1
#MAG_YMIN = -1

# < the end >--------------------------------------------------------------------------------------
